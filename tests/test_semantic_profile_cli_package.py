from pathlib import Path


def test_semantic_profiles_cli_exists():
    assert Path("excel_builder_semantic_profiles.py").exists()


def test_build_excel_report_runs_semantic_profiles():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_semantic_profiles.py" in text
    assert "semantic_profile_console.txt" in text


def test_zip_includes_semantic_profile_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "semantic_profile_report.txt" in text
    assert "semantic_profiles.csv" in text
