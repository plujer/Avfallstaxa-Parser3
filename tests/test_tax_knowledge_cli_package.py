from pathlib import Path


def test_tax_knowledge_cli_exists():
    assert Path("excel_builder_tax_knowledge.py").exists()


def test_build_excel_report_runs_tax_knowledge_step():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_tax_knowledge.py" in text
    assert "tax_knowledge_console.txt" in text


def test_zip_includes_tax_knowledge_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "tax_knowledge_report.txt" in text
    assert "tax_knowledge_features.csv" in text
