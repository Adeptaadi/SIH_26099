from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_evaluation_metrics():
    response = client.get("/api/evaluation/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_pairs" in data
    assert "accuracy" in data
    assert "precision" in data
    assert "recall" in data
    assert "f1_score" in data
    assert "confusion_matrix" in data

def test_get_ablation():
    response = client.get("/api/evaluation/ablation")
    assert response.status_code == 200
    data = response.json()
    assert "methods" in data
    assert len(data["methods"]) == 4

def test_get_hard_negatives():
    response = client.get("/api/demo/hard-negatives")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
