from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.models import ParserTaxRow, StandardTaxCatalog, StandardTaxRow
from excel_builder.semantic import SemanticProfileIndex, TaxSemanticProfileEngine


def test_tax_semantic_profile_engine_creates_word_profile():
    knowledge = TaxKnowledgeExtractor().extract([
        ParserTaxRow(section="2.1", tax_point="Kärl 190 L restavfall", unit="")
    ])

    report = TaxSemanticProfileEngine().from_knowledge_report(knowledge)
    profile = report.profiles[0]

    assert profile.source == "WORD"
    assert profile.key.container_type == "Kärl"
    assert profile.key.container_volume_liter == "190"
    assert profile.key.waste_type == "Restavfall"


def test_tax_semantic_profile_engine_creates_standard_profile():
    catalog = StandardTaxCatalog(source_path="standard.xlsx", rows=[
        StandardTaxRow(
            source_sheet="Standard Avfall",
            row_number=2,
            strTaxekod="KÄ190RE",
            strTaxebenamning="Kärl 190 L restavfall",
            strFaktor="VOLYM/BEHÅLLARE",
        )
    ])

    report = TaxSemanticProfileEngine().from_standard_catalog(catalog)
    profile = report.profiles[0]

    assert profile.source == "STANDARD"
    assert profile.standard_tax_code == "KÄ190RE"
    assert profile.key.container_type == "Kärl"
    assert profile.key.container_volume_liter == "190"


def test_semantic_profile_index_scores_related_profiles():
    engine = TaxSemanticProfileEngine()
    word = engine.from_knowledge_report(TaxKnowledgeExtractor().extract([
        ParserTaxRow(section="2.1", tax_point="Kärl 190 L restavfall", unit="")
    ])).profiles[0]
    standard = engine.from_standard_catalog(StandardTaxCatalog(source_path="standard.xlsx", rows=[
        StandardTaxRow(
            source_sheet="Standard Avfall",
            row_number=2,
            strTaxekod="KÄ190RE",
            strTaxebenamning="Kärl 190 L restavfall",
            strFaktor="VOLYM/BEHÅLLARE",
        )
    ])).profiles[0]

    score = SemanticProfileIndex([standard]).score(word, standard)

    assert score >= 0.5
