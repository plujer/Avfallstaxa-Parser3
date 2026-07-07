from pathlib import Path


def test_standard_catalog_scan_cli_exists():
    assert Path("excel_builder_standard_catalog_scan.py").exists()


def test_build_excel_report_runs_standard_catalog_scan():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_standard_catalog_scan.py" in text
    assert "standard_catalog_schema_console.txt" in text


def test_zip_includes_standard_catalog_scan_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "standard_catalog_schema_report.txt" in text
    assert "EDP_Standardtaxor_normalized.xlsx" in text
