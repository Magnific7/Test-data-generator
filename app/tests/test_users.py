from app.generators.users import generate_user, generate_users
from app.models.users import User


def test_generate_single_user():

    user = generate_user(1)

    assert isinstance(user, User)
    assert user.id == 1
    assert user.name
    assert user.email
    assert user.phone


def test_generate_multiple_users():

    users = generate_users(10)

    assert len(users) == 10

    for user in users:
        assert isinstance(user, User)


def test_user_ids_are_unique():

    users = generate_users(10)

    ids = [user.id for user in users]

    assert len(ids) == len(set(ids))