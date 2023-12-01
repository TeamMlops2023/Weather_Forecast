import sys
sys.path.insert(0, '../src')

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# test de l'endpoint run_model
def test_metrics_endpoint():
    response = client.get("/run_model")
    assert response.status_code == 200
    assert "model_execution_count" in response.text
