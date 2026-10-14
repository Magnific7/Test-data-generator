from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

MAX_RECORDS = 1000


def _check_total(scenarios: dict) -> None:
    total = sum(scenarios.values())
    if total > MAX_RECORDS:
        raise ValueError(f"Total count across scenarios must be at most {MAX_RECORDS}, got {total}")


class UserScenario(str, Enum):
    """
    Allowed scenarios for generating users.
    """
    VALID = "valid"
    INVALID_EMAIL = "invalid-email"
    MISSING_REQUIRED_FIELD = "missing-required-field"
    DUPLICATE_VALUES = "duplicate-values"
    BOUNDARY = "boundary"
    MIXED = "mixed"


class GenerateUserRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"count": 10, "scenario": "invalid-email"}]}
    )

    count: int = Field(gt=0, le=MAX_RECORDS)
    scenario: UserScenario = UserScenario.VALID


class GenerateMixedUserRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "scenarios": {
                        "valid": 5,
                        "invalid-email": 3,
                        "missing-required-field": 2,
                        "duplicate-values": 3,
                        "boundary": 1,
                    }
                }
            ]
        }
    )

    scenarios: dict[UserScenario, PositiveInt] = Field(min_length=1)

    @model_validator(mode="after")
    def check_total(self):
        _check_total(self.scenarios)
        return self


class InvoiceScenario(str, Enum):
    """
    Allowed scenarios for generating invoices.
    """
    VALID = "valid"
    ZERO_AMOUNT = "zero-amount"
    NEGATIVE_AMOUNT = "negative-amount"
    TAX_GREATER_THAN_TOTAL = "tax-greater-than-total"
    DEDUCTIONS_GREATER_THAN_TOTAL = "deductions-greater-than-total"
    MIXED = "mixed"


class GenerateInvoiceRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"count": 10, "scenario": "tax-greater-than-total"}]}
    )

    count: int = Field(gt=0, le=MAX_RECORDS)
    scenario: InvoiceScenario = InvoiceScenario.VALID


class GenerateMixedInvoiceRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "scenarios": {
                        "valid": 5,
                        "zero-amount": 3,
                        "negative-amount": 3,
                        "tax-greater-than-total": 4,
                        "deductions-greater-than-total": 2,
                    }
                }
            ]
        }
    )

    scenarios: dict[InvoiceScenario, PositiveInt] = Field(min_length=1)

    @model_validator(mode="after")
    def check_total(self):
        _check_total(self.scenarios)
        return self
