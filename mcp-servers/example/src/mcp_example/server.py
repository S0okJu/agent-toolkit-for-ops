from mcp.server.mcpserver import MCPServer

from mcp_example.tools import health

mcp = MCPServer("example")
health.register(mcp)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
