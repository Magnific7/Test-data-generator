from typer.testing import CliRunner

from app.cli import app

runner = CliRunner()


def test_users_console_valid_scenario():
    result = runner.invoke(app, ["users", "5"])

    assert result.exit_code == 0
    assert "5 valid, 0 invalid" in result.output


def test_users_console_invalid_email_scenario():
    result = runner.invoke(app, ["users", "3", "--scenario", "invalid-email"])

    assert result.exit_code == 0
    assert "0 valid, 3 invalid" in result.output


def test_invoices_console_business_rule_violation():
    result = runner.invoke(app, ["invoices", "2", "--scenario", "tax-greater-than-total"])

    assert result.exit_code == 0
    assert "business rule violated" in result.output


def test_users_unknown_scenario_exits_with_error():
    result = runner.invoke(app, ["users", "1", "--scenario", "not-a-real-scenario"])

    assert result.exit_code != 0


def test_users_csv_export_writes_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["users", "3", "--format", "csv"])

    assert result.exit_code == 0
    assert (tmp_path / "users.csv").exists()


def test_invoices_json_export_writes_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["invoices", "3", "--scenario", "valid", "--format", "json"])

    assert result.exit_code == 0
    assert (tmp_path / "invoices.json").exists()
