"""Register / unregister this repo's MCP servers with local Claude Code and Codex.

Usage:
    uv run scripts/mcpctl.py list
    uv run scripts/mcpctl.py add [NAME ...]       # no NAME = all servers
    uv run scripts/mcpctl.py remove [NAME ...]    # no NAME = all servers
    ... --agent claude|codex                      # default: every installed agent

A server is any `mcp-servers/<name>/` package that defines a `[project.scripts]`
entry. It is registered under `<name>` as a stdio server launched through
`uv run`, so code changes take effect without re-registering.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SERVERS_DIR = REPO_ROOT / "mcp-servers"
AGENTS = ("claude", "codex")


@dataclass
class Server:
    name: str
    package: str
    script: str

    def launch_command(self, uv: str) -> list[str]:
        return [uv, "run", "--quiet", "--directory", str(REPO_ROOT),
                "--package", self.package, self.script]


def discover_servers() -> dict[str, Server]:
    servers = {}
    for pyproject in sorted(SERVERS_DIR.glob("*/pyproject.toml")):
        project = tomllib.loads(pyproject.read_text()).get("project", {})
        scripts = project.get("scripts", {})
        if scripts:
            name = pyproject.parent.name
            servers[name] = Server(name, project["name"], next(iter(scripts)))
    return servers


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def registered(agent: str) -> set[str]:
    if agent == "claude":
        config = Path.home() / ".claude.json"
        if not config.exists():
            return set()
        return set(json.loads(config.read_text()).get("mcpServers", {}))
    result = run(["codex", "mcp", "list", "--json"])
    return {s["name"] for s in json.loads(result.stdout or "[]")}


def add(agent: str, server: Server, uv: str) -> subprocess.CompletedProcess:
    remove(agent, server.name)  # make add idempotent and refresh the command
    if agent == "claude":
        cmd = ["claude", "mcp", "add", "-s", "user", server.name, "--"]
    else:
        cmd = ["codex", "mcp", "add", server.name, "--"]
    return run(cmd + server.launch_command(uv))


def remove(agent: str, name: str) -> subprocess.CompletedProcess:
    if agent == "claude":
        return run(["claude", "mcp", "remove", "-s", "user", name])
    return run(["codex", "mcp", "remove", name])


def main() -> None:
    parser = argparse.ArgumentParser(prog="mcpctl", description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["list", "add", "remove"])
    parser.add_argument("names", nargs="*", help="server names (default: all)")
    parser.add_argument("--agent", choices=AGENTS, action="append",
                        help="target agent (repeatable; default: all installed)")
    args = parser.parse_args()

    servers = discover_servers()
    if unknown := set(args.names) - set(servers):
        sys.exit(f"unknown server(s): {', '.join(sorted(unknown))} "
                 f"(available: {', '.join(servers) or 'none'})")
    targets = [servers[n] for n in args.names] if args.names else list(servers.values())

    agents = []
    for agent in args.agent or AGENTS:
        if shutil.which(agent):
            agents.append(agent)
        else:
            print(f"skip {agent}: CLI not found on PATH", file=sys.stderr)

    if args.command == "list":
        status = {agent: registered(agent) for agent in agents}
        for server in targets:
            marks = "  ".join(f"{a}:{'on' if server.name in status[a] else 'off'}"
                              for a in agents)
            print(f"{server.name:<20} {marks}")
        return

    uv = shutil.which("uv")
    if args.command == "add" and not uv:
        sys.exit("uv not found on PATH")

    failed = False
    for agent in agents:
        for server in targets:
            if args.command == "add":
                result = add(agent, server, uv)
            else:
                if server.name not in registered(agent):
                    print(f"{agent:<7} {server.name}: not registered")
                    continue
                result = remove(agent, server.name)
            ok = result.returncode == 0
            failed |= not ok
            detail = "" if ok else f" -> {(result.stderr or result.stdout).strip()}"
            print(f"{agent:<7} {args.command} {server.name}: {'ok' if ok else 'FAILED'}{detail}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
