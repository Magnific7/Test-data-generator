import typer

from app.generators import generate_invoice_records, generate_user_records
from app.models.invoices import Invoice
from app.models.users import User
from app.models.validation import validate_records
from app.reporting import export_outcomes, print_console

app = typer.Typer(
    name="test-data-generator",
    help="A CLI tool to generate schema-validated QA test data.",
)

FORMAT_OPTION = typer.Option("console", "--format", "-f", help="Output format: console, json, or csv")
SCENARIO_OPTION = typer.Option("valid", "--scenario", "-s", help="QA scenario to generate")


@app.command()
def users(
    count: int = typer.Argument(..., help="Number of users to generate"),
    scenario: str = SCENARIO_OPTION,
    format: str = FORMAT_OPTION,
) -> None:
    """Generate schema-validated test users for a given QA scenario."""

    print(f"\nGenerating {count} users (scenario: {scenario})...\n")

    try:
        records = generate_user_records(count, scenario)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    outcomes = validate_records(User, records)

    if format == "console":
        print_console(outcomes, scenario)
    elif format in ("csv", "json"):
        filename = export_outcomes(outcomes, format, "users")
        print(f"✓ Data saved to {filename}")
    else:
        typer.echo(f"Unsupported format: {format}. Please choose 'console', 'json' or 'csv'.", err=True)
        raise typer.Exit(code=1)


@app.command()
def invoices(
    count: int = typer.Argument(..., help="Number of invoices to generate"),
    scenario: str = SCENARIO_OPTION,
    format: str = FORMAT_OPTION,
) -> None:
    """Generate schema- and business-rule-validated test invoices for a given QA scenario."""

    print(f"\nGenerating {count} invoices (scenario: {scenario})...\n")

    try:
        records = generate_invoice_records(count, scenario)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    outcomes = validate_records(Invoice, records)

    if format == "console":
        print_console(outcomes, scenario)
    elif format in ("csv", "json"):
        filename = export_outcomes(outcomes, format, "invoices")
        print(f"✓ Data saved to {filename}")
    else:
        typer.echo(f"Unsupported format: {format}. Please choose 'console', 'json' or 'csv'.", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
