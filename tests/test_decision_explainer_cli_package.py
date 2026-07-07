from pathlib import Path


def test_decision_explainer_cli_exists():
    assert Path("excel_builder_decision_explainer.py").exists()


def test_build_excel_report_runs_explainable_decision_engine():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_decision_explainer.py" in text
    assert "explainable_decision_console.txt" in text


def test_zip_includes_explainable_decision_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "explainable_decision_report.txt" in text
    assert "decision_traces.csv" in text
