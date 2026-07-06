from excel_builder.knowledge import KnowledgeIndexBuilder, TaxKnowledgeExtractor
from excel_builder.models import ParserTaxRow, StandardTaxCatalog, StandardTaxRow


def test_knowledge_index_builder_groups_word_and_standard_rows():
    knowledge = TaxKnowledgeExtractor().extract([
        ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")
    ])
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

    index = KnowledgeIndexBuilder().build(knowledge, catalog)

    assert index.entry_count >= 1
    assert index.standard_row_count == 1
    assert any(entry.feature_count == 1 for entry in index.entries.values())
    assert any(len(entry.standard_rows) == 1 for entry in index.entries.values())


def test_knowledge_index_candidate_entries_for_feature_returns_related_entries():
    knowledge = TaxKnowledgeExtractor().extract([
        ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")
    ])
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

    builder = KnowledgeIndexBuilder()
    index = builder.build(knowledge, catalog)
    candidates = builder.candidate_entries_for_feature(index, knowledge.features[0])

    assert candidates
