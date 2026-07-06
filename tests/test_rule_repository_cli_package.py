from pathlib import Path


def test_rule_repository_cli_exists():
    assert Path("excel_builder_rule_repository.py").exists()


def test_build_excel_report_runs_rule_repository():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_rule_repository.py" in text
    assert "master_rule_repository_console.txt" in text


def test_zip_includes_rule_repository_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "master_rule_repository_report.txt" in text
    assert "master_rule_repository.csv" in text
