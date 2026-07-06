from excel_builder.models import ParserTaxRow, WorkbookTaxRow
from excel_builder.validation import WordTaxCoverageValidator


def test_word_tax_coverage_passes_when_word_tax_exists_in_taxepunkter():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = [WorkbookTaxRow(row_number=2, section="6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="kilogram", tax_code="", proposed_price="")]

    report = WordTaxCoverageValidator().validate(parser_rows, workbook_rows)

    assert report.passed
    assert report.covered == 1
    assert report.missing == 0


def test_word_tax_coverage_fails_when_word_tax_missing_even_if_edp_is_empty():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = []

    report = WordTaxCoverageValidator().validate(parser_rows, workbook_rows)

    assert not report.passed
    assert report.missing == 1
    assert "oavsett EDP" in report.items[0].comment


def test_word_tax_coverage_accepts_existing_row_without_tax_code():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = [WorkbookTaxRow(row_number=2, section="§6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="kilogram", tax_code="", proposed_price="")]

    report = WordTaxCoverageValidator().validate(parser_rows, workbook_rows)

    assert report.passed
    assert report.covered == 1
