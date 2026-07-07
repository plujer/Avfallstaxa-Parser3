from pathlib import Path


def test_semantic_attributes_cli_exists():
    assert Path("excel_builder_semantic_attributes.py").exists()


def test_build_excel_report_runs_semantic_attributes():
    content = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_semantic_attributes.py" in content


def test_zip_includes_semantic_attribute_reports():
    content = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "semantic_attribute_report.txt" in content or "output\\excel" in content
