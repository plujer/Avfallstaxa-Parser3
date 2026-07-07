from pathlib import Path


def test_context_resolve_cli_exists():
    assert Path("excel_builder_context_resolve.py").exists()


def test_build_excel_report_runs_context_resolver():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_context_resolve.py" in text
    assert "context_resolution_console.txt" in text


def test_zip_includes_context_resolution_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "context_resolution_report.txt" in text
    assert "context_resolved_rows.csv" in text
