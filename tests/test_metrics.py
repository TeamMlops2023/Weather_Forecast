import sys
sys.path.insert(0, '../src')

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# test de l'endpoint metrics
def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "model_execution_count" in response.text
