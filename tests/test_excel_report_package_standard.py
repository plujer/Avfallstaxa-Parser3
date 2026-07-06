from pathlib import Path


def test_excel_report_zip_includes_expected_core_files():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")

    expected = [
        "ArbetsExcel_byggd_fran_parser.xlsx",
        "excel_matching_results.csv",
        "excel_matching_report.txt",
        "arbets_excel_profile_report.txt",
        "arbets_excel_snapshot.txt",
        "pytest_report.txt",
        "parser3_result.json",
        "parser3_acceptance_report.txt",
        "excel_report_manifest.txt",
    ]

    for item in expected:
        assert item in text


def test_build_excel_report_creates_snapshot_before_zip():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_snapshot.py" in text
    assert "Skapar standardiserad rapportzip" in text
    assert "Skicka senaste ZIP-filen från rapportzip" in text
