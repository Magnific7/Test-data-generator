import pytest

from app.generators.invoices import generate_invoice_records
from app.models.invoices import Invoice
from app.models.validation import validate_records


def test_valid_scenario_produces_business_valid_invoices():
    records = generate_invoice_records(5, "valid")
    outcomes = validate_records(Invoice, records)

    assert len(outcomes) == 5
    assert all(outcome.is_valid for outcome in outcomes)
    assert all(outcome.instance.is_business_valid for outcome in outcomes)


def test_zero_amount_scenario_is_schema_and_business_valid():
    records = generate_invoice_records(2, "zero-amount")
    outcomes = validate_records(Invoice, records)

    assert all(outcome.is_valid for outcome in outcomes)
    assert all(outcome.instance.amount_payable == 0.0 for outcome in outcomes)


def test_negative_amount_scenario_fails_schema_validation():
    records = generate_invoice_records(2, "negative-amount")
    outcomes = validate_records(Invoice, records)

    assert all(not outcome.is_valid for outcome in outcomes)
    assert all("total_amount" in outcome.error for outcome in outcomes)


def test_tax_greater_than_total_scenario_is_schema_valid_but_business_invalid():
    records = generate_invoice_records(2, "tax-greater-than-total")
    outcomes = validate_records(Invoice, records)

    assert all(outcome.is_valid for outcome in outcomes)
    assert all(not outcome.instance.is_business_valid for outcome in outcomes)


def test_deductions_greater_than_total_scenario_is_schema_valid_but_business_invalid():
    records = generate_invoice_records(2, "deductions-greater-than-total")
    outcomes = validate_records(Invoice, records)

    assert all(outcome.is_valid for outcome in outcomes)
    assert all(not outcome.instance.is_business_valid for outcome in outcomes)


def test_invoice_numbers_are_sequential():
    records = generate_invoice_records(3, "valid")

    assert [r["invoice_number"] for r in records] == ["INV-1001", "INV-1002", "INV-1003"]


def test_mixed_scenario_dispatches_to_the_chosen_sub_scenario(monkeypatch):
    from app.scenarios import invoices as invoice_scenarios

    monkeypatch.setattr(invoice_scenarios.random, "choice", lambda pool: "negative-amount")

    records = generate_invoice_records(3, "mixed")

    assert all(record["total_amount"] < 0 for record in records)


def test_mixed_scenario_produces_a_mix_of_business_valid_and_invalid():
    records = generate_invoice_records(40, "mixed")
    outcomes = validate_records(Invoice, records)

    schema_valid = [o for o in outcomes if o.is_valid]
    assert any(o.instance.is_business_valid for o in schema_valid)
    assert any(not o.instance.is_business_valid for o in schema_valid)


def test_unknown_scenario_raises():
    with pytest.raises(ValueError, match="does-not-exist"):
        generate_invoice_records(1, "does-not-exist")
