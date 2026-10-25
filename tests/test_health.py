from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_reports_degraded_without_a_model():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "DEGRADED", "activeModel": None}
