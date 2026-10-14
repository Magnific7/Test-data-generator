from app.scenarios.invoices import INVOICE_SCENARIOS


def generate_invoice_records(count: int, scenario: str = "valid") -> list[dict]:
    """Generate raw (possibly invalid) invoice records for a named QA scenario."""
    if scenario not in INVOICE_SCENARIOS:
        raise ValueError(
            f"Unknown invoice scenario '{scenario}'. Available: {', '.join(sorted(INVOICE_SCENARIOS))}"
        )

    builder = INVOICE_SCENARIOS[scenario]
    return [
        {"invoice_number": f"INV-{1000 + i}", **builder()}
        for i in range(1, count + 1)
    ]


def generate_mixed_invoice_records(scenario_counts: dict[str, int]) -> list[dict]:
    """Generate an exact number of invoice records per scenario, each tagged with its scenario."""
    records = []
    for scenario, count in scenario_counts.items():
        for record in generate_invoice_records(count, scenario):
            records.append({**record, "scenario": scenario})

    for i, record in enumerate(records, start=1):
        record["invoice_number"] = f"INV-{1000 + i}"

    return records
