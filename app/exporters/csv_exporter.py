import csv


def export_csv(data: list[dict], filename: str) -> None:
    """
    Export data to a CSV file.
    """

    if not data:
        return

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=data[0].keys()
        )

        writer.writeheader()
        writer.writerows(data)