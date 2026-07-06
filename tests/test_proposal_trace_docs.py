from pathlib import Path


def test_block_docs_mention_proposal_and_trace_sheets():
    text = Path("docs/ExcelBuilder_Block14_ProposalAndTraceSheets.md").read_text(encoding="utf-8")
    assert "Taxa_Förslag" in text
    assert "Regelspårning" in text


def test_isolated_builder_mentions_trace_sheets():
    text = Path("excel_builder/edp/isolated_workbook_builder.py").read_text(encoding="utf-8")
    assert "Taxa_Förslag" in text
    assert "Regelspårning" in text
