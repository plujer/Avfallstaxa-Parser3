from pathlib import Path


def test_knowledge_index_cli_exists():
    assert Path("excel_builder_knowledge_index.py").exists()


def test_build_excel_report_runs_knowledge_index():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "excel_builder_knowledge_index.py" in text
    assert "knowledge_index_console.txt" in text


def test_zip_includes_knowledge_index_reports():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")
    assert "knowledge_index_report.txt" in text
    assert "knowledge_index.csv" in text
