from pathlib import Path


def test_decision_cli_exists():
    assert Path("excel_builder_decide.py").exists()


def test_build_excel_report_runs_decision_engine():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_decide.py" in text
    assert "tax_decision_console.txt" in text


def test_zip_includes_decision_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "tax_decision_report.txt" in text
    assert "tax_decision_results.csv" in text
