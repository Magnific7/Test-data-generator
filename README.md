# Test Data Generator

A command-line tool for generating realistic fake user data for development and testing.

## Features

- Generates realistic fake users with unique numeric IDs, names, email addresses, and phone numbers.
- Prints generated users directly to the console by default.
- Exports generated users to CSV or JSON files when requested.
- Supports configurable user counts from the command line.

## Installation

Requires Python 3.11 or newer.

```bash
python -m venv .env
source .env/bin/activate
python -m pip install -e ".[dev]"
```

## Usage

Generate one or more users in the console:

```bash
testdata 5
```

Export generated users to CSV:

```bash
testdata 5 --format csv
```

This creates `users.csv` in the current directory.

Export generated users to JSON:

```bash
testdata 5 --format json
```

This creates `users.json` in the current directory.

The short option `-f` can also be used:

```bash
testdata 5 -f json
```

## Testing

Run the test suite with:

```bash
pytest
```

## Project Structure

```text
app/
  cli.py                 CLI entry point
  exporters/             CSV and JSON exporters
  generators/            Fake user data generation
tests/                   Automated tests
pyproject.toml           Project metadata and dependencies
```

CSV and JSON files generated during local use, along with build and package metadata directories, are excluded by `.gitignore`.
