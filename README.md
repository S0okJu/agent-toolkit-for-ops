# agent-toolkit-for-ops

A collection of **MCP servers** and **skills** for system operations.
Works with both Claude Code and Codex on your local machine.

## Layout

```
agent-toolkit-for-ops/
├── mcp-servers/
│   ├── common/          # Logic shared across servers (mcp-common)
│   └── <target>/        # One MCP server per target system (e.g. kubernetes, prometheus)
├── skills/
│   └── <task>/          # One skill per ops task (e.g. incident-triage)
├── scripts/
│   └── mcpctl.py        # Register/unregister MCP servers locally
├── tests/               # Repo-wide tests (skill portability checks, etc.)
└── docs/
```

## Getting started

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv sync --all-packages   # Install the whole workspace
uv run pytest            # Run tests
```

## MCP servers

### Register with local agents

`scripts/mcpctl.py` calls the `claude mcp` / `codex mcp` CLIs to register servers.
Claude Code servers are added at user scope, so they are available in every project.

```sh
uv run scripts/mcpctl.py list                 # Show registration status
uv run scripts/mcpctl.py add                  # Register all servers
uv run scripts/mcpctl.py add kubernetes       # Register specific servers
uv run scripts/mcpctl.py remove               # Unregister all servers
uv run scripts/mcpctl.py add --agent codex    # Target a single agent
```

Servers are registered to launch via `uv run`, so code changes take effect without re-registering.
Run `remove` before deleting a server's folder.

### Adding a server

Copy `mcp-servers/example` to start. Name servers after the **target system** they connect to.

| Item | Convention | Example |
|---|---|---|
| Folder | `mcp-servers/<target>` | `mcp-servers/kubernetes` |
| Package / command | `mcp-<target>` | `mcp-kubernetes` |
| Import name | `mcp_<target>` | `mcp_kubernetes` |
| Tool module | `tools/<feature>.py` | `tools/pods.py` |

- `server.py` only assembles the server; tools live in `tools/` modules and register via `register(mcp)`.
- Logic used by two or more servers goes in `mcp-servers/common`.
- Uses MCP Python SDK 2.x (`from mcp.server.mcpserver import MCPServer`).

## Skills

A single `SKILL.md` is shared by Claude Code and Codex. Name skills after the **task** they perform.

```
skills/<name>/
├── SKILL.md              # frontmatter: name, description
├── agents/openai.yaml    # Codex-only settings (optional)
├── scripts/
└── references/
```

Portability rules are enforced by `tests/test_skills.py`:

- `name`: kebab-case, at most 64 characters, matches the folder name
- `description`: at most 1024 characters
- Frontmatter keys: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`

### Link to local agents

```sh
ln -s "$PWD/skills/<name>" ~/.claude/skills/   # Claude Code
ln -s "$PWD/skills/<name>" ~/.agents/skills/   # Codex
```
