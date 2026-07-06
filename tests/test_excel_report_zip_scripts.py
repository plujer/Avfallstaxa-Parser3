from pathlib import Path


def test_excel_report_zip_script_exists_and_targets_rapportzip():
    path = Path("tools/zip_excel_report.ps1")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "$zipDir = "rapportzip"" in text
    assert "ExcelBuilder_Run_" in text


def test_build_excel_report_bat_exists():
    path = Path("build_excel_report.bat")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Skicka senaste ZIP-filen från rapportzip" in text
    assert "zip_excel_report.ps1" in text
