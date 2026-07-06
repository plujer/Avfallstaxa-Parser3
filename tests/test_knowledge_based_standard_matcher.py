from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.models import ParserTaxRow, StandardTaxCatalog, StandardTaxRow
from excel_builder.standard import KnowledgeBasedStandardMatcher, StandardTaxSuggestionEngine


def test_knowledge_based_standard_matcher_finds_asbest_weight_match():
    features = TaxKnowledgeExtractor().extract([
        ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")
    ]).features

    catalog = StandardTaxCatalog(source_path="standard.xlsx", rows=[
        StandardTaxRow(
            source_sheet="Standard Avfall",
            row_number=2,
            strTaxekod="STD-ASB",
            strTaxebenamning="Asbest emballerat",
            strFaktor="VIKG",
            strTaxedelAvser="Kilogram",
        )
    ])

    matches = KnowledgeBasedStandardMatcher().match(features, catalog)

    assert matches[0].status == "PROPOSAL"
    assert matches[0].standard_row.strTaxekod == "STD-ASB"
    assert matches[0].score >= 0.72


def test_standard_tax_suggestion_engine_uses_knowledge_matching_by_default():
    parser_rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]
    catalog = StandardTaxCatalog(source_path="standard.xlsx", rows=[
        StandardTaxRow(
            source_sheet="Standard Avfall",
            row_number=2,
            strTaxekod="STD-ASB",
            strTaxebenamning="Asbest emballerat",
            strFaktor="VIKG",
            strTaxedelAvser="Kilogram",
        )
    ])

    report = StandardTaxSuggestionEngine().suggest(parser_rows, catalog)

    assert report.proposal_count == 1
    assert report.suggestions[0].method == "Knowledge weighted standard match"


def test_knowledge_matcher_keeps_weak_match_as_no_suggestion():
    features = TaxKnowledgeExtractor().extract([
        ParserTaxRow(section="6.1.2", tax_point="Helt okänd taxa", unit="styck")
    ]).features

    catalog = StandardTaxCatalog(source_path="standard.xlsx", rows=[
        StandardTaxRow(
            source_sheet="Standard Slam",
            row_number=2,
            strTaxekod="STD-SLAM",
            strTaxebenamning="Slamtömning extra",
            strFaktor="TILLFÄLLE",
        )
    ])

    matches = KnowledgeBasedStandardMatcher().match(features, catalog)

    assert matches[0].status == "NO_SUGGESTION"
