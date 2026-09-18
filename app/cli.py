import typer

from app.generators import generate_users, generate_user


app = typer.Typer(
    name="test-data-generator",
    help="A CLI tool to generate test data for users.",
)

@app.command()
def users(num_users: int = typer.Argument(..., help="Number of users to generate")):
    """Generate a specified number of random users."""
    users = generate_users(num_users)
    for user in users:
        typer.echo(user)   

    print(f"Generated {num_users} users.")


if __name__ == "__main__":
    app()