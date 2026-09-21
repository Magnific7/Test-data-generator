from faker import Faker

from app.models.users import User
from app.scenarios.users import USER_SCENARIOS

faker = Faker()

def generate_user(user_id: int) -> User:
    """Generate a random user with name, email, and phone."""
    user = User(
    id=user_id,
    name=faker.name(),
    email=faker.email(),
    phone=faker.phone_number(),
)
    return user

def generate_users(count: int) -> list:
    """Generate a list of random users."""
    users = []
    for user_id in range(1, count + 1):
        user = generate_user(user_id)
        users.append(user)
    return users


def generate_user_records(count: int, scenario: str = "valid") -> list[dict]:
    """Generate raw (possibly invalid) user records for a named QA scenario."""
    if scenario not in USER_SCENARIOS:
        raise ValueError(
            f"Unknown user scenario '{scenario}'. Available: {', '.join(sorted(USER_SCENARIOS))}"
        )

    builder = USER_SCENARIOS[scenario]
    records = [{"id": user_id, **builder()} for user_id in range(1, count + 1)]

    if scenario == "duplicate-values" and records:
        shared_email = records[0]["email"]
        for record in records:
            record["email"] = shared_email

    return records