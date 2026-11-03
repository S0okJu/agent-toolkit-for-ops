from mcp_example.tools.health import ping


def test_ping():
    assert ping() == "pong"
