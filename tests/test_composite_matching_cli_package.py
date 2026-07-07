from pathlib import Path


def test_composite_matching_cli_exists():
    assert Path("excel_builder_composite_matching.py").exists()


def test_build_excel_report_runs_composite_matching():
    content = Path("build_excel_report.bat").read_text(encoding="utf-8", errors="ignore")
    assert "excel_builder_composite_matching.py" in content


def test_zip_includes_composite_matching_reports():
    content = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8", errors="ignore")
    assert "composite_matching_report.txt" in content
    assert "composite_matches.csv" in content
