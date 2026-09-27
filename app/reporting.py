import os

from app.exporters.csv_exporter import export_csv
from app.exporters.json_exporter import export_to_json
from app.models.invoices import Invoice
from app.models.validation import ValidationOutcome


def _format_record(data: dict) -> str:
    return " ".join(f"{key}={value!r}" for key, value in data.items())


def _enrich(outcome: ValidationOutcome) -> dict:
    row = dict(outcome.data)
    row["valid"] = outcome.is_valid
    row["errors"] = outcome.error or ""

    if isinstance(outcome.instance, Invoice):
        row["amount_payable"] = outcome.instance.amount_payable
        row["business_valid"] = outcome.instance.is_business_valid

    return row


def print_console(outcomes: list[ValidationOutcome], scenario: str) -> None:
    valid_count = 0

    for outcome in outcomes:
        if not outcome.is_valid:
            print(f"✗ {_format_record(outcome.data)}")
            print(f"    └─ {outcome.error}")
            continue

        valid_count += 1
        if isinstance(outcome.instance, Invoice) and not outcome.instance.is_business_valid:
            print(
                f"⚠ {_format_record(outcome.data)} amount_payable={outcome.instance.amount_payable!r}"
                "  [business rule violated: amount_payable is negative]"
            )
        else:
            print(f"✓ {_format_record(outcome.data)}")

    invalid_count = len(outcomes) - valid_count
    print(f"\n{valid_count} valid, {invalid_count} invalid (scenario: {scenario})")


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def export_outcomes(outcomes: list[ValidationOutcome], export_format: str, filename_prefix: str) -> str:
    rows = [_enrich(outcome) for outcome in outcomes]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{filename_prefix}.{export_format}")

    if export_format == "csv":
        export_csv(rows, filepath)
    else:
        export_to_json(rows, filepath)

    return filepath
