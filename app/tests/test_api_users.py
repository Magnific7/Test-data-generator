import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.api.schemas.requests import UserScenario
from app.scenarios.users import USER_SCENARIOS


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


def test_unknown_scenario_returns_422():
    response = client.post("/users", json={"count": 2, "scenario": "bogus"})

    assert response.status_code == 422


def test_user_scenario_enum_matches_generator():
    assert {scenario.value for scenario in UserScenario} == set(USER_SCENARIOS)


@pytest.mark.parametrize("scenario", [scenario.value for scenario in UserScenario])
def test_every_scenario_generates_users(scenario):
    response = client.post("/users", json={"count": 3, "scenario": scenario})

    assert response.status_code == 200
    assert response.json()["scenario"] == scenario


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


def test_generate_mixed_users():
    response = client.post(
        "/users/mixed",
        json={
            "scenarios": {
                "valid": 3,
                "invalid-email": 3,
                "missing-required-field": 4,
            },
        },
    )

    assert response.status_code == 200

    body = response.json()
    scenarios = [user["scenario"] for user in body["data"]]

    assert body["count"] == 10
    assert scenarios.count("valid") == 3
    assert scenarios.count("invalid-email") == 3
    assert scenarios.count("missing-required-field") == 4


def test_mixed_user_ids_are_unique():
    response = client.post(
        "/users/mixed",
        json={"scenarios": {"valid": 3, "boundary": 3}},
    )

    ids = [user["id"] for user in response.json()["data"]]

    assert ids == [1, 2, 3, 4, 5, 6]


@pytest.mark.parametrize(
    "scenarios",
    [
        {},
        {"valid": 0},
        {"valid": -1},
        {"bogus": 2},
        {"valid": 600, "boundary": 401},
    ],
)
def test_invalid_mixed_user_request_returns_422(scenarios):
    response = client.post("/users/mixed", json={"scenarios": scenarios})

    assert response.status_code == 422
