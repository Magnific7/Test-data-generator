from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.routes.users import router as users_router

app = FastAPI(
    title="Test Data Generator API",
    description="API for generating synthetic QA test data",
    version="1.0.0",
)

client = TestClient(app)

app.include_router(users_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-health")
def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}