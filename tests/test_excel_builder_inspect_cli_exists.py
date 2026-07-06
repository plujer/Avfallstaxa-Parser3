from pathlib import Path


def test_excel_builder_inspect_cli_exists():
    assert Path("excel_builder_inspect.py").exists()
    assert Path("inspect_excel.bat").exists()


def test_build_excel_runs_inspect_step():
    text = Path("build_excel.bat").read_text(encoding="utf-8")
    assert "excel_builder_inspect.py" in text
    assert "Arbets-Excel" in text
