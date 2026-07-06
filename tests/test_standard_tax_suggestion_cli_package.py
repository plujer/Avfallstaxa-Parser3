from pathlib import Path


def test_standard_suggestions_cli_exists():
    assert Path("excel_builder_standard_suggestions.py").exists()


def test_build_excel_report_runs_standard_suggestions():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_standard_suggestions.py" in text
    assert "standard_tax_suggestions_console.txt" in text


def test_zip_includes_standard_suggestion_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "standard_tax_suggestions_report.txt" in text
    assert "standard_tax_suggestions.csv" in text
