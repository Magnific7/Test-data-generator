# Test Data Generator

A command-line tool that generates realistic fake data for testing — users and invoices —
including data that's deliberately **broken on purpose**, so you can check that a system
correctly accepts good data and rejects bad data.

## Why this exists

When testing software, you don't just need normal, everyday data. You also need:

- data that *should* be accepted (a real name, a real email address)
- data that *should* be rejected (a broken email, a missing name)
- edge cases (an invoice worth exactly $0)
- data that breaks a business rule even though it "looks" fine (an invoice where the tax
  charged is somehow bigger than the invoice total)

Making all of that up by hand is slow and repetitive. This tool generates it for you, on
demand, and tells you clearly whether each record it made is valid or not — then lets you
export it as a CSV or JSON file to use elsewhere.

## Installation

Requires Python 3.11 or newer.

```bash
python -m venv .env
source .env/bin/activate
python -m pip install -e ".[dev]"
```

## Usage

Generate 10 normal, valid users:

```bash
testdata users 10
```

Generate users with a deliberately broken email address, to test that bad data gets rejected:

```bash
testdata users 10 --scenario invalid-email
```

Generate invoices, and generate invoices for a specific "bad data" case:

```bash
testdata invoices 20 --scenario valid
testdata invoices 20 --scenario tax-greater-than-total
```

Every command works the same way and accepts two options:

- `--scenario` (or `-s`) — which kind of data to generate (see the tables below). Defaults to `valid`.
- `--format` (or `-f`) — how to output it: `console` (default, prints to screen), `csv`, or `json`.

```bash
testdata users 5 --scenario boundary --format csv        # writes users.csv
testdata invoices 5 --scenario zero-amount --format json  # writes invoices.json
```

In the console, each record is marked ✓ (good), ✗ (rejected, with the reason why), or ⚠ (looks
fine but breaks a business rule) — followed by a summary line. The CSV/JSON files include every
record generated, good or bad, with extra columns saying whether it passed and why — that's
often the whole point, since you can feed a batch of intentionally bad data straight into
whatever system you're testing to confirm it correctly says no.

## Supported scenarios

### `users`

| Scenario | What you get |
|---|---|
| `valid` (default) | A normal, fully valid user. |
| `invalid-email` | A user with a broken email address. |
| `missing-required-field` | A user with their name left out entirely. |
| `duplicate-values` | A batch of users who all share the same email address. |
| `boundary` | A user with an empty name — right at the edge of what's allowed. |
| `mixed` | A single batch with a random blend of the scenarios above. |

### `invoices`

Every invoice follows one rule: **amount you actually pay = total − tax − other deductions.**

| Scenario | What you get |
|---|---|
| `valid` (default) | A normal invoice where the amount payable comes out positive. |
| `zero-amount` | An invoice where everything is zero — still technically valid. |
| `negative-amount` | An invoice with a negative total, which should be rejected outright. |
| `tax-greater-than-total` | An invoice where the tax alone is bigger than the total — looks fine on paper, but breaks the payment rule. |
| `deductions-greater-than-total` | Same idea, but the deductions are what's too large. |
| `mixed` | A single batch with a random blend of the scenarios above. |

## Running the tests

```bash
pytest
```
