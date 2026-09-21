import csv


def export_csv(data: list, filename: str) -> None:
    """
    Export data to a CSV file.
    """

    if not data:
        return

    rows = [row.model_dump() if hasattr(row, "model_dump") else row for row in data]

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)