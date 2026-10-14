from enum import Enum

from pydantic import BaseModel, Field


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
    count: int = Field(gt=0, le=1000)
    scenario: UserScenario = UserScenario.VALID
