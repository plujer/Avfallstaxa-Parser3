from pathlib import Path


def test_standard_tax_file_path_is_documented_in_package():
    assert Path("data/edp_standard").exists()


def test_zip_report_includes_standard_tax_source():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "EDP_Future_Standard_Taxor_Renhallning.xlsx" in text


def test_edp_run_report_mentions_standard_tax_reference():
    text = Path("excel_builder/reports/edp_run_reporter.py").read_text(encoding="utf-8")
    assert "STANDARDTAXOR" in text
    assert "referensflikar" in text


def test_standard_tax_can_only_be_reference_not_override():
    text = Path("excel_builder/edp/proposal_trace_sheets.py").read_text(encoding="utf-8")
    assert "Taxa_från_edp" in text
    assert "ändras aldrig automatiskt" in text
    assert "EDP_Avviker_Standard" in text
