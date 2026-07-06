from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.models import ParserTaxRow


def test_tax_knowledge_extractor_detects_avc_weight_asbest():
    rows = [ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram")]

    report = TaxKnowledgeExtractor().extract(rows)
    feature = report.features[0]

    assert feature.category == "ÅVC/verksamhetsavfall"
    assert feature.waste_type == "Asbest"
    assert feature.unit_type == "Vikt"
    assert feature.factor_hint == "VIKG"
    assert feature.confidence > 0.8


def test_tax_knowledge_extractor_detects_container_volume():
    rows = [ParserTaxRow(section="2.1", tax_point="Kärl 190 L restavfall", unit="")]

    report = TaxKnowledgeExtractor().extract(rows)
    feature = report.features[0]

    assert feature.category == "Hushåll"
    assert feature.waste_type == "Restavfall"
    assert feature.unit_type == "Behållarvolym"
    assert feature.container_volume_liter == "190"


def test_tax_knowledge_extractor_detects_slam_category():
    rows = [ParserTaxRow(section="5.1", tax_point="Slamtömning extra", unit="tillfälle")]

    report = TaxKnowledgeExtractor().extract(rows)
    feature = report.features[0]

    assert feature.category == "Slam"
    assert feature.waste_type == "Slam"
    assert feature.factor_hint == "TILLFÄLLE"
