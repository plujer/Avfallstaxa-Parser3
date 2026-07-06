from pathlib import Path


def test_tax_knowledge_cli_supports_workbook_argument():
    text = Path("excel_builder_tax_knowledge.py").read_text(encoding="utf-8")
    assert "--workbook" in text
    assert "KnowledgeWorkbookWriter" in text


def test_build_excel_report_writes_tax_knowledge_to_workbook():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "Skriver Tax Knowledge till Arbets-Excel" in text
    assert "--workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx"" in text
