import random

_MIXED_POOL = [
    "valid",
    "zero-amount",
    "negative-amount",
    "tax-greater-than-total",
    "deductions-greater-than-total",
]


def valid_invoice() -> dict:
    """A fully valid invoice: tax and deductions comfortably within the total."""
    total = round(random.uniform(50, 500), 2)
    tax = round(total * 0.1, 2)
    deductions = round(random.uniform(0, total * 0.05), 2)
    return {"total_amount": total, "mandatory_tax": tax, "other_deductions": deductions}


def zero_amount_invoice() -> dict:
    """Boundary scenario: everything at zero, payable lands exactly on the valid/invalid edge."""
    return {"total_amount": 0.0, "mandatory_tax": 0.0, "other_deductions": 0.0}


def negative_amount_invoice() -> dict:
    """Negative scenario: total_amount fails schema validation (must be >= 0)."""
    return {"total_amount": -50.0, "mandatory_tax": 0.0, "other_deductions": 0.0}


def tax_greater_than_total_invoice() -> dict:
    """Negative scenario: schema-valid but violates the amount_payable business rule."""
    total = 100.0
    return {"total_amount": total, "mandatory_tax": total + 50, "other_deductions": 0.0}


def deductions_greater_than_total_invoice() -> dict:
    """Negative scenario: schema-valid but violates the amount_payable business rule."""
    total = 100.0
    return {"total_amount": total, "mandatory_tax": 0.0, "other_deductions": total + 50}


def mixed_invoice() -> dict:
    """Each record is randomly drawn from the other invoice scenarios."""
    scenario = random.choice(_MIXED_POOL)
    return INVOICE_SCENARIOS[scenario]()


INVOICE_SCENARIOS = {
    "valid": valid_invoice,
    "zero-amount": zero_amount_invoice,
    "negative-amount": negative_amount_invoice,
    "tax-greater-than-total": tax_greater_than_total_invoice,
    "deductions-greater-than-total": deductions_greater_than_total_invoice,
    "mixed": mixed_invoice,
}
