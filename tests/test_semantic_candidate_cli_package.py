from pathlib import Path


def test_semantic_candidate_cli_exists():
    assert Path("excel_builder_semantic_candidates.py").exists()


def test_build_excel_report_runs_semantic_candidate_ranking():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_semantic_candidates.py" in text
    assert "semantic_candidate_console.txt" in text


def test_zip_includes_semantic_candidate_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "semantic_candidate_report.txt" in text
    assert "semantic_candidates.csv" in text
