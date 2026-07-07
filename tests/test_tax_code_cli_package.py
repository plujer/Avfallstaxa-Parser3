from pathlib import Path


def test_tax_code_cli_exists():
    assert Path("excel_builder_tax_codes.py").exists()


def test_build_excel_report_runs_tax_code_intelligence():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_tax_codes.py" in text
    assert "tax_code_intelligence_console.txt" in text


def test_zip_includes_tax_code_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "tax_code_intelligence_report.txt" in text
    assert "tax_code_intelligence.csv" in text
