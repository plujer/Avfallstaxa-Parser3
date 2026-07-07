from pathlib import Path

def test_schema_scan_cli_exists():
    assert Path("excel_builder_schema_scan.py").exists()

def test_build_excel_report_runs_schema_scan_before_rule_repository():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_schema_scan.py" in text
    assert "workbook_schema_console.txt" in text
    assert text.index("excel_builder_schema_scan.py") < text.index("excel_builder_rule_repository.py")

def test_zip_includes_schema_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "workbook_schema_report.txt" in text
    assert "workbook_schema_sheets.csv" in text
    assert "workbook_schema_header_candidates.csv" in text
