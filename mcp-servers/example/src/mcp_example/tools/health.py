from mcp.server.mcpserver import MCPServer


def ping() -> str:
    """Return 'pong' to confirm the server is alive."""
    return "pong"


def register(mcp: MCPServer) -> None:
    mcp.tool()(ping)
