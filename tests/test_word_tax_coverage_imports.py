from pathlib import Path

from excel_builder.models import CoverageItem, CoverageReport, ParserTaxRow, WorkbookTaxRow
from excel_builder.reports import CoverageReporter
from excel_builder.validation import WordTaxCoverageValidator


def test_coverage_modules_import_cleanly():
    parser_row = ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")
    workbook_row = WorkbookTaxRow(row_number=2, section="6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="kilogram", tax_code="", proposed_price="")

    item = CoverageItem(parser_row=parser_row, workbook_row=workbook_row, status="COVERED", method="test")
    report = CoverageReport(items=[item])

    assert report.covered == 1
    assert WordTaxCoverageValidator is not None
    assert CoverageReporter is not None


def test_coverage_cli_exists():
    assert Path("excel_builder_coverage.py").exists()
