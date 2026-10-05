from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(
    title="Test Data Generator API",
    description="API for generating synthetic QA test data",
    version="1.0.0",
)

client = TestClient(app)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-health")
def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}