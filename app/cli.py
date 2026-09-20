import typer

from app.generators import generate_users
from app.exporters.json_exporter import export_to_json
from app.exporters.csv_exporter import export_csv


app = typer.Typer(
    name="test-data-generator",
    help="A CLI tool to generate test data for users.",
)

@app.command()
def users(num_users: int = typer.Argument(..., help="Number of users to generate"), 
        format: str = typer.Option(
        "console",
        "--format",
        "-f",
        help="Output format: console, json, or csv"
         )):

    """Generate a specified number of random users."""

    print(f"\nGenerating {num_users} users...\n")

    users = generate_users(num_users)

    if format == "console":
        for user in users:
            typer.echo(user)

        print(f"Generated {num_users} users.")

    elif format == "csv":

        filename = "users.csv"

        export_csv(users, filename)

        print(f"✓ Data saved to {filename}")

    elif format == "json":
            file_path = "users.json"
            export_to_json(users, file_path)
            print(f"Users exported to {file_path}.")

    else:
        print(f"Unsupported format: {format}. Please choose 'json', 'csv' or 'console'.")


if __name__ == "__main__":
    app()