from excel_builder.models import ParserTaxRow, WorkbookTaxRow
from excel_builder.word_excel_mapping import WordExcelMappingEngine


def test_word_excel_mapping_creates_stable_ids_and_exact_mapping():
    parser_rows = [ParserTaxRow(section="2.1", tax_point="Grundavgift", variant="Villa", unit="kr")]
    workbook_rows = [WorkbookTaxRow(row_number=6, section="2.1", paragraph_name="Grundavgifter", tax_point="Grundavgift", variant="Villa", unit="kr", tax_code="G001", proposed_price="")]

    report = WordExcelMappingEngine().build(parser_rows, workbook_rows)

    assert report.passed
    assert report.mapped == 1
    assert report.items[0].word_tax_id.startswith("WTX-2-1-")
    assert report.items[0].workbook_row.row_number == 6


def test_word_excel_mapping_duplicate_edp_tax_code_is_allowed_not_error():
    parser_rows = [
        ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="14 dagar", unit="kr"),
        ParserTaxRow(section="2.2.2", tax_point="Kärl 240 l", variant="14 dagar", unit="kr"),
    ]
    workbook_rows = [
        WorkbookTaxRow(row_number=10, section="2.2.1", paragraph_name="", tax_point="Kärl 240 l", variant="14 dagar", unit="kr", tax_code="KÄ240RM26", proposed_price=""),
        WorkbookTaxRow(row_number=11, section="2.2.2", paragraph_name="", tax_point="Kärl 240 l", variant="14 dagar", unit="kr", tax_code="KÄ240RM26", proposed_price=""),
    ]

    report = WordExcelMappingEngine().build(parser_rows, workbook_rows)

    assert report.missing == 0
    assert report.review == 0
    assert all(item.status == "MAPPED" for item in report.items)
    assert all(item.duplicate_edp_allowed for item in report.items)
    assert all("tillåtet" in item.comment for item in report.items)


def test_word_excel_mapping_marks_missing_word_tax():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest", variant="", unit="kg")]
    report = WordExcelMappingEngine().build(parser_rows, [])

    assert not report.passed
    assert report.missing == 1
    assert report.items[0].status == "MISSING"


def test_word_excel_mapping_stable_identity_survives_section_move():
    original = ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="14 dagar", unit="kr")
    moved = ParserTaxRow(section="2.2.9", tax_point="Kärl 240 l", variant="14 dagar", unit="kr")

    report = WordExcelMappingEngine().build([original, moved], [])

    assert report.items[0].word_tax_id != report.items[1].word_tax_id
    assert report.items[0].stable_tax_identity == report.items[1].stable_tax_identity
    assert report.items[0].content_fingerprint == report.items[1].content_fingerprint
    assert "Stabil identitet" in report.items[0].comment
    assert "inte automatiskt fel" in report.items[0].comment


def test_word_excel_mapping_stable_identity_changes_when_variant_changes():
    first = ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="14 dagar", unit="kr")
    second = ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="månadsvis", unit="kr")

    report = WordExcelMappingEngine().build([first, second], [])

    assert report.items[0].stable_tax_identity != report.items[1].stable_tax_identity
    assert report.items[0].content_fingerprint != report.items[1].content_fingerprint
