import pytest
from pydantic import ValidationError

from app.models.invoices import Invoice


def test_amount_payable_is_computed_from_the_business_rule():
    invoice = Invoice(
        invoice_number="INV-1001",
        total_amount=100.0,
        mandatory_tax=10.0,
        other_deductions=5.0,
    )

    assert invoice.amount_payable == 85.0
    assert invoice.is_business_valid


def test_zero_amount_is_a_valid_boundary():
    invoice = Invoice(
        invoice_number="INV-1002",
        total_amount=0.0,
        mandatory_tax=0.0,
        other_deductions=0.0,
    )

    assert invoice.amount_payable == 0.0
    assert invoice.is_business_valid


def test_tax_greater_than_total_violates_business_rule_but_not_schema():
    invoice = Invoice(
        invoice_number="INV-1003",
        total_amount=100.0,
        mandatory_tax=150.0,
        other_deductions=0.0,
    )

    assert invoice.amount_payable == -50.0
    assert not invoice.is_business_valid


def test_deductions_greater_than_total_violates_business_rule_but_not_schema():
    invoice = Invoice(
        invoice_number="INV-1004",
        total_amount=100.0,
        mandatory_tax=0.0,
        other_deductions=150.0,
    )

    assert invoice.amount_payable == -50.0
    assert not invoice.is_business_valid


def test_negative_total_amount_fails_schema_validation():
    with pytest.raises(ValidationError):
        Invoice(
            invoice_number="INV-1005",
            total_amount=-50.0,
            mandatory_tax=0.0,
            other_deductions=0.0,
        )
