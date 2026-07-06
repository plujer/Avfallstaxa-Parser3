from pathlib import Path


def test_word_tax_coverage_cli_exists():
    assert Path("excel_builder_coverage.py").exists()


def test_build_excel_report_runs_coverage_step():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_coverage.py" in text
    assert "alla Word-taxor finns i Taxepunkter" in text


def test_zip_excel_report_includes_coverage_files():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "word_tax_coverage_report.txt" in text
    assert "word_tax_coverage_results.csv" in text
