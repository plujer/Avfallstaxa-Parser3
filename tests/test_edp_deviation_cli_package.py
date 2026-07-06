from pathlib import Path


def test_edp_deviation_cli_exists():
    assert Path("excel_builder_edp_deviations.py").exists()


def test_build_excel_report_runs_edp_deviation_analysis():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_edp_deviations.py" in text
    assert "EDP_Future_Standard_Taxor_Renhallning.xlsx" in text
    assert "Sorsele.xlsx" in text
