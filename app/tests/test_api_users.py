import pytest
from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200


def test_generate_valid_users():
    response = client.post(
        "/users",
        json={
            "count": 3,
            "scenario": "valid",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 3
    assert body["scenario"] == "valid"
    assert len(body["data"]) == 3


def test_scenario_defaults_to_valid():
    response = client.post("/users", json={"count": 2})

    assert response.status_code == 200
    assert response.json()["scenario"] == "valid"


def test_unknown_scenario_returns_400():
    response = client.post("/users", json={"count": 2, "scenario": "bogus"})

    assert response.status_code == 400
    assert "Unknown user scenario" in response.json()["detail"]


@pytest.mark.parametrize("count", [0, -1, 1001])
def test_count_out_of_range_returns_422(count):
    response = client.post("/users", json={"count": count})

    assert response.status_code == 422


def test_missing_count_returns_422():
    response = client.post("/users", json={"scenario": "valid"})

    assert response.status_code == 422


def test_generate_invalid_email_users():
    response = client.post(
        "/users",
        json={
            "count": 3,
            "scenario": "invalid-email",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 3
    assert body["scenario"] == "invalid-email"

    for user in body["data"]:
        assert "@" not in user["email"]


def test_count_cannot_exceed_limit():
    response = client.post(
        "/users",
        json={
            "count": 1001,
            "scenario": "valid",
        },
    )

    assert response.status_code == 422


def test_count_must_be_greater_than_zero():
    response = client.post(
        "/users",
        json={
            "count": 0,
            "scenario": "valid",
        },
    )

    assert response.status_code == 422


def test_count_cannot_be_negative():
    response = client.post(
        "/users",
        json={
            "count": -1,
            "scenario": "valid",
        },
    )

    assert response.status_code == 422