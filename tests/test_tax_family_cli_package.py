from pathlib import Path


def test_tax_family_cli_exists():
    assert Path("excel_builder_tax_family.py").exists()


def test_build_excel_report_runs_tax_family_step():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")

    assert "excel_builder_tax_family.py" in text
    assert "tax_family_console.txt" in text


def test_zip_includes_tax_family_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")

    assert "output\\excel\\tax_family_report.txt" in text
    assert "output\\excel\\tax_families.csv" in text
