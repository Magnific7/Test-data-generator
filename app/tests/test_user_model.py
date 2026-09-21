import pytest
from pydantic import ValidationError

from app.models.users import User


def test_valid_user_constructs():
    user = User(id=1, name="Jane Doe", email="jane@example.com", phone="555-1234")

    assert user.id == 1
    assert user.email == "jane@example.com"


def test_invalid_email_is_rejected():
    with pytest.raises(ValidationError):
        User(id=1, name="Jane Doe", email="not-an-email", phone="555-1234")


def test_missing_required_field_is_rejected():
    with pytest.raises(ValidationError):
        User(id=1, email="jane@example.com", phone="555-1234")


def test_id_boundary_zero_is_rejected():
    with pytest.raises(ValidationError):
        User(id=0, name="Jane Doe", email="jane@example.com", phone="555-1234")


def test_empty_name_boundary_is_rejected():
    with pytest.raises(ValidationError):
        User(id=1, name="", email="jane@example.com", phone="555-1234")
