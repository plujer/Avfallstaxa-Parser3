from excel_builder.builder import TaxepunkterRowBuilder
from excel_builder.models import ParserTaxRow, WorkbookTaxRow


def test_taxepunkter_row_builder_creates_row_when_word_tax_missing():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = []

    plan = TaxepunkterRowBuilder().build_plan(parser_rows, workbook_rows)

    assert plan.total_parser_rows == 1
    assert plan.create_count == 1
    assert plan.rows[0].action == "CREATE"
    assert "oavsett EDP" in plan.rows[0].comment


def test_taxepunkter_row_builder_reuses_existing_row_without_tax_code():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = [WorkbookTaxRow(row_number=10, section="§6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="kilogram", tax_code="", proposed_price="")]

    plan = TaxepunkterRowBuilder().build_plan(parser_rows, workbook_rows)

    assert plan.reuse_count == 1
    assert plan.create_count == 0
    assert plan.rows[0].excel_row_number == 10


def test_taxepunkter_row_builder_has_one_plan_row_per_parser_row():
    parser_rows = [
        ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram"),
        ParserTaxRow(section="6.1.2", tax_point="Ny taxa", unit="styck"),
    ]
    workbook_rows = [WorkbookTaxRow(row_number=10, section="6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="kilogram", tax_code="", proposed_price="")]

    plan = TaxepunkterRowBuilder().build_plan(parser_rows, workbook_rows)

    assert plan.total_parser_rows == len(parser_rows)
    assert plan.reuse_count == 1
    assert plan.create_count == 1
