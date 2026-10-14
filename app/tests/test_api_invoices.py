import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.api.schemas.requests import InvoiceScenario
from app.scenarios.invoices import INVOICE_SCENARIOS


client = TestClient(app)


def test_generate_valid_invoices():
    response = client.post(
        "/invoices",
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
    response = client.post("/invoices", json={"count": 2})

    assert response.status_code == 200
    assert response.json()["scenario"] == "valid"


def test_unknown_scenario_returns_422():
    response = client.post("/invoices", json={"count": 2, "scenario": "bogus"})

    assert response.status_code == 422


def test_invoice_scenario_enum_matches_generator():
    assert {scenario.value for scenario in InvoiceScenario} == set(INVOICE_SCENARIOS)


@pytest.mark.parametrize("scenario", [scenario.value for scenario in InvoiceScenario])
def test_every_scenario_generates_invoices(scenario):
    response = client.post("/invoices", json={"count": 3, "scenario": scenario})

    assert response.status_code == 200
    assert response.json()["scenario"] == scenario


@pytest.mark.parametrize("count", [0, -1, 1001])
def test_count_out_of_range_returns_422(count):
    response = client.post("/invoices", json={"count": count})

    assert response.status_code == 422


def test_missing_count_returns_422():
    response = client.post("/invoices", json={"scenario": "valid"})

    assert response.status_code == 422


def test_generate_negative_amount_invoices():
    response = client.post(
        "/invoices",
        json={
            "count": 3,
            "scenario": "negative-amount",
        },
    )

    assert response.status_code == 200

    for invoice in response.json()["data"]:
        assert invoice["total_amount"] < 0


def test_generate_tax_greater_than_total_invoices():
    response = client.post(
        "/invoices",
        json={
            "count": 3,
            "scenario": "tax-greater-than-total",
        },
    )

    assert response.status_code == 200

    for invoice in response.json()["data"]:
        assert invoice["mandatory_tax"] > invoice["total_amount"]


def test_generate_mixed_invoices():
    response = client.post(
        "/invoices/mixed",
        json={
            "scenarios": {
                "zero-amount": 3,
                "negative-amount": 3,
                "tax-greater-than-total": 4,
            },
        },
    )

    assert response.status_code == 200

    body = response.json()
    scenarios = [invoice["scenario"] for invoice in body["data"]]

    assert body["count"] == 10
    assert scenarios.count("zero-amount") == 3
    assert scenarios.count("negative-amount") == 3
    assert scenarios.count("tax-greater-than-total") == 4


def test_mixed_invoice_numbers_are_unique():
    response = client.post(
        "/invoices/mixed",
        json={"scenarios": {"valid": 3, "zero-amount": 3}},
    )

    invoice_numbers = [invoice["invoice_number"] for invoice in response.json()["data"]]

    assert len(invoice_numbers) == len(set(invoice_numbers))


@pytest.mark.parametrize(
    "scenarios",
    [
        {},
        {"valid": 0},
        {"valid": -1},
        {"bogus": 2},
        {"valid": 600, "zero-amount": 401},
    ],
)
def test_invalid_mixed_invoice_request_returns_422(scenarios):
    response = client.post("/invoices/mixed", json={"scenarios": scenarios})

    assert response.status_code == 422
