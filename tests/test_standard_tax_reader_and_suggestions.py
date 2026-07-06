from openpyxl import Workbook

from excel_builder.models import ParserTaxRow
from excel_builder.standard import StandardTaxReader, StandardTaxSuggestionEngine


def create_standard_tax_file(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Standard Avfall"
    ws.append(["strTaxekod", "strTaxebenamning", "strFaktor", "strTaxedelAvser", "strFormel"])
    ws.append(["KOD1", "Asbest, emballerat", "VIKG", "Kilogram", "FORMEL1"])
    ws.append(["KOD2", "Träavfall behandlat", "VIKG", "Kilogram", "FORMEL2"])
    wb.save(path)


def test_standard_tax_reader_reads_catalog(tmp_path):
    path = tmp_path / "standard.xlsx"
    create_standard_tax_file(path)

    catalog = StandardTaxReader().read(path)

    assert catalog.row_count == 2
    assert catalog.rows[0].strTaxekod == "KOD1"
    assert catalog.rows[0].strTaxebenamning == "Asbest, emballerat"


def test_standard_tax_suggestion_engine_finds_proposal(tmp_path):
    path = tmp_path / "standard.xlsx"
    create_standard_tax_file(path)

    catalog = StandardTaxReader().read(path)
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]

    report = StandardTaxSuggestionEngine().suggest(parser_rows, catalog)

    assert report.total == 1
    assert report.proposal_count == 1
    assert report.suggestions[0].standard_row.strTaxekod == "KOD1"


def test_standard_tax_suggestion_engine_marks_no_suggestion(tmp_path):
    path = tmp_path / "standard.xlsx"
    create_standard_tax_file(path)

    catalog = StandardTaxReader().read(path)
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Helt okänd taxa", unit="styck")]

    report = StandardTaxSuggestionEngine().suggest(parser_rows, catalog)

    assert report.total == 1
    assert report.no_suggestion_count == 1
