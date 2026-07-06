from pathlib import Path


def test_apply_suggestions_cli_exists():
    assert Path("excel_builder_apply_suggestions.py").exists()


def test_build_excel_report_applies_suggestions_to_workbooks():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_apply_suggestions.py" in text
    assert "Skriver standardtaxeförslag till Arbets-Excel" in text
    assert "ArbetsExcel_Sorsele_byggd.xlsx" in text
