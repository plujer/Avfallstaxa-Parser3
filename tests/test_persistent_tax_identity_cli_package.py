from pathlib import Path


def test_persistent_tax_identity_cli_exists():
    assert Path("excel_builder_persistent_tax_identity.py").exists()


def test_build_excel_report_runs_persistent_tax_identity():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_persistent_tax_identity.py" in text
    assert "persistent_tax_identity_console.txt" in text


def test_zip_includes_persistent_tax_identity_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "persistent_tax_identity_report.txt" in text
    assert "persistent_tax_identity.csv" in text
