from pydantic import BaseModel, Field, model_validator


class Invoice(BaseModel):
    invoice_number: str
    total_amount: float = Field(ge=0)
    mandatory_tax: float = Field(ge=0)
    other_deductions: float = Field(ge=0)
    amount_payable: float = 0

    @model_validator(mode="after")
    def _compute_amount_payable(self) -> "Invoice":
        self.amount_payable = round(
            self.total_amount - self.mandatory_tax - self.other_deductions, 2
        )
        return self

    @property
    def is_business_valid(self) -> bool:
        """Business rule: the payable amount must not be negative."""
        return self.amount_payable >= 0
