from pathlib import Path


def test_excel_builder_match_cli_exists():
    assert Path("excel_builder_match.py").exists()


def test_build_excel_report_runs_matching_preview():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_match.py" in text
    assert "excel_matching_console.txt" in text
