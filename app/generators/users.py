from faker import Faker

faker = Faker()

def generate_user(user_id: int) -> dict:
    """Generate a random user with name, email, and phone."""
    user = {
        "id": user_id,
        "name": faker.name(),
        "email": faker.email(),
        "phone": faker.phone_number()
    }
    return user

def generate_users(count: int) -> list:
    """Generate a list of random users."""
    users = []
    for user_id in range(1, count + 1):
        user = generate_user(user_id)
        users.append(user)
    return users