from excel_builder.decision import TaxDecisionEngine
from excel_builder.models import ParserTaxRow, StandardTaxRow, StandardTaxSuggestion, StandardTaxSuggestionReport, WorkbookTaxRow


def test_decision_engine_prefers_existing_edp_match():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = [WorkbookTaxRow(row_number=10, section="6.1.2", paragraph_name="", tax_point="Asbest, emballerat", variant="", unit="kilogram", tax_code="EDP1", proposed_price="")]
    suggestions = StandardTaxSuggestionReport(suggestions=[
        StandardTaxSuggestion(
            parser_row=parser_rows[0],
            standard_row=StandardTaxRow(source_sheet="Standard", row_number=2, strTaxekod="STD1", strTaxebenamning="Asbest, emballerat"),
            status="PROPOSAL",
            score=0.99,
            method="test",
        )
    ])

    report = TaxDecisionEngine().decide(parser_rows, workbook_rows, suggestions)

    assert report.edp_match == 1
    assert report.standard_proposal == 0
    assert report.decisions[0].workbook_row.tax_code == "EDP1"


def test_decision_engine_uses_standard_only_when_no_edp_match():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    workbook_rows = []
    suggestions = StandardTaxSuggestionReport(suggestions=[
        StandardTaxSuggestion(
            parser_row=parser_rows[0],
            standard_row=StandardTaxRow(source_sheet="Standard", row_number=2, strTaxekod="STD1", strTaxebenamning="Asbest, emballerat"),
            status="PROPOSAL",
            score=0.99,
            method="test",
        )
    ])

    report = TaxDecisionEngine().decide(parser_rows, workbook_rows, suggestions)

    assert report.standard_proposal == 1
    assert report.decisions[0].standard_row.strTaxekod == "STD1"


def test_decision_engine_marks_new_taxa_without_match_or_suggestion():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Ny taxa", unit="styck")]

    report = TaxDecisionEngine().decide(parser_rows, [], None)

    assert report.new_taxa == 1
    assert report.decisions[0].status == "NEW_TAXA"
