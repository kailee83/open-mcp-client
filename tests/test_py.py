from fastapi.testclient import TestClient
from open_mcp_client.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Open MCP Client!"}

def test_run_command():
    response = client.post("/command", json={"command": "run"})
    assert response.status_code == 200
    assert response.json() == {"status": "Command received", "data": {"command": "run"}}
