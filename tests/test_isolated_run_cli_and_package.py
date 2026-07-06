from pathlib import Path


def test_isolated_run_cli_exists():
    assert Path("excel_builder_isolated_run.py").exists()


def test_build_sorsele_excel_bat_exists():
    assert Path("build_sorsele_excel.bat").exists()
    text = Path("build_sorsele_excel.bat").read_text(encoding="utf-8")
    assert "Sorsele.xlsx" in text


def test_all_edp_exports_are_kept_separate():
    text = Path("build_all_edp_exports.bat").read_text(encoding="utf-8")
    assert "Mala.xlsx" in text
    assert "Norsjo.xlsx" in text
    assert "Sorsele.xlsx" in text
    assert "--municipality" in text
