from pathlib import Path


def test_row_plan_cli_exists():
    assert Path("excel_builder_row_plan.py").exists()


def test_build_excel_report_runs_row_plan_step():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_row_plan.py" in text
    assert "Taxepunkter row plan" in text


def test_zip_excel_report_includes_row_plan_files():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "taxepunkter_row_plan_report.txt" in text
    assert "taxepunkter_row_plan.csv" in text
