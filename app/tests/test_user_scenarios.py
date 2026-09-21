import pytest

from app.generators.users import generate_user_records
from app.models.users import User
from app.models.validation import validate_records


def test_valid_scenario_produces_valid_users():
    records = generate_user_records(5, "valid")
    outcomes = validate_records(User, records)

    assert len(outcomes) == 5
    assert all(outcome.is_valid for outcome in outcomes)


def test_invalid_email_scenario_fails_validation():
    records = generate_user_records(3, "invalid-email")
    outcomes = validate_records(User, records)

    assert all(not outcome.is_valid for outcome in outcomes)
    assert all("email" in outcome.error for outcome in outcomes)


def test_missing_required_field_scenario_omits_name():
    records = generate_user_records(3, "missing-required-field")

    assert all("name" not in record for record in records)

    outcomes = validate_records(User, records)
    assert all(not outcome.is_valid for outcome in outcomes)


def test_duplicate_values_scenario_shares_one_email():
    records = generate_user_records(4, "duplicate-values")

    emails = {record["email"] for record in records}
    assert len(emails) == 1

    ids = {record["id"] for record in records}
    assert len(ids) == 4


def test_boundary_scenario_produces_empty_name():
    records = generate_user_records(2, "boundary")

    assert all(record["name"] == "" for record in records)

    outcomes = validate_records(User, records)
    assert all(not outcome.is_valid for outcome in outcomes)


def test_mixed_scenario_dispatches_to_the_chosen_sub_scenario(monkeypatch):
    from app.scenarios import users as users_scenarios

    monkeypatch.setattr(users_scenarios.random, "choice", lambda pool: "missing-required-field")

    records = generate_user_records(3, "mixed")

    assert all("name" not in record for record in records)


def test_mixed_scenario_produces_a_mix_of_valid_and_invalid():
    records = generate_user_records(40, "mixed")
    outcomes = validate_records(User, records)

    assert any(outcome.is_valid for outcome in outcomes)
    assert any(not outcome.is_valid for outcome in outcomes)


def test_unknown_scenario_raises():
    with pytest.raises(ValueError, match="does-not-exist"):
        generate_user_records(1, "does-not-exist")
