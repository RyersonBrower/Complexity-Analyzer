import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyzer.app import app

def test_analyze_loop_request():
    client = app.test_client()
    response = client.post("/analyze", json={"code": "for i in range(n): print(i)"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["recurrence_detected"]["type"] == "loop"
    assert "big_o_hint" in data

def test_analyze_empty_request():
    client = app.test_client()
    response = client.post("/analyze", json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
