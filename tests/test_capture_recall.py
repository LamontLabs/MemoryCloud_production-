from fastapi.testclient import TestClient
from src.memorycloud.api import app

client = TestClient(app)

def test_capture_and_recall_flow():
    payload = {"text": "unit test entry", "indicator": True}
    resp = client.post("/capture", json=payload)
    assert resp.status_code == 200
    recall = client.get("/recall")
    assert recall.status_code == 200
    data = recall.json()
    assert any("unit test entry" in item["text"] for item in data["matches"])
