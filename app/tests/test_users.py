from app.generators.users import generate_user, generate_users


def test_generate_single_user():

    user = generate_user(1)

    assert user["id"] == 1
    assert "name" in user
    assert "email" in user
    assert "phone" in user


def test_generate_multiple_users():

    users = generate_users(10)

    assert len(users) == 10


def test_user_ids_are_unique():

    users = generate_users(10)

    ids = [user["id"] for user in users]

    assert len(ids) == len(set(ids))