import random

from faker import Faker

faker = Faker()

_MIXED_POOL = ["valid", "invalid-email", "missing-required-field", "boundary"]


def _base_user() -> dict:
    return {
        "name": faker.name(),
        "email": faker.email(),
        "phone": faker.phone_number(),
    }


def valid_user() -> dict:
    """A fully valid user record."""
    return _base_user()


def invalid_email_user() -> dict:
    """Negative scenario: email fails schema validation."""
    user = _base_user()
    user["email"] = "not-an-email"
    return user


def missing_required_field_user() -> dict:
    """Negative scenario: a required field is absent entirely."""
    user = _base_user()
    del user["name"]
    return user


def duplicate_values_user() -> dict:
    """Negative scenario: batch-level uniqueness violation, forced by the generator."""
    return _base_user()


def boundary_user() -> dict:
    """Boundary scenario: name at the empty-string edge of the min_length constraint."""
    user = _base_user()
    user["name"] = ""
    return user


def mixed_user() -> dict:
    """Each record is randomly drawn from the other per-record scenarios."""
    scenario = random.choice(_MIXED_POOL)
    return USER_SCENARIOS[scenario]()


USER_SCENARIOS = {
    "valid": valid_user,
    "invalid-email": invalid_email_user,
    "missing-required-field": missing_required_field_user,
    "duplicate-values": duplicate_values_user,
    "boundary": boundary_user,
    "mixed": mixed_user,
}
