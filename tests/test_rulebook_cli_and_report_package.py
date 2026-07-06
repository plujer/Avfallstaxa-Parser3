from pathlib import Path


def test_rulebook_cli_exists():
    assert Path("excel_builder_rulebook.py").exists()


def test_build_excel_report_runs_rulebook_step():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_rulebook.py" in text
    assert "edp_rulebook_report.txt" in text


def test_zip_excel_report_includes_rulebook_report():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "edp_rulebook_report.txt" in text
    assert "edp_rulebook_console.txt" in text
