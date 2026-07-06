from excel_builder.matching import MatchingEngine
from excel_builder.models import ParserTaxRow, WorkbookTaxRow


def test_matching_engine_exact_match():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = [WorkbookTaxRow(row_number=10, section="6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="kilogram", tax_code="KOD1", proposed_price="")]

    report = MatchingEngine().match(parser_rows, workbook_rows)

    assert report.exact == 1
    assert report.candidates[0].workbook_row.tax_code == "KOD1"


def test_matching_engine_new_when_no_match():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Ny taxa", unit="styck")]
    workbook_rows = []

    report = MatchingEngine().match(parser_rows, workbook_rows)

    assert report.new == 1
    assert report.candidates[0].status == "NEW"


def test_matching_engine_probable_when_variant_or_unit_differs():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = [WorkbookTaxRow(row_number=10, section="6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="", tax_code="KOD1", proposed_price="")]

    report = MatchingEngine().match(parser_rows, workbook_rows)

    assert report.probable == 1
