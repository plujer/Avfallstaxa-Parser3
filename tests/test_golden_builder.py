from parser3.golden import FacitRow, GoldenMasterBuilder, GoldenMasterMerger
from parser3.rules import SectionRuleEngine, ReferenceRuleEngine, VariantRuleEngine
from parser3.matching import ConfidenceScoring, TaxPatternMatcher
from parser3.models import TaxRow


def test_golden_master_builder_counts_rows():
    rows = [
        FacitRow(section="6.1.2", name="Asbest", unit="kilogram"),
        FacitRow(section="6.1.2", name="Toner utan elektronik", export=False, comment="reference"),
    ]
    data = GoldenMasterBuilder().build(rows)
    assert data["sections"]["6.1.2"]["tax_count"] == 1


def test_golden_master_merger_avoids_duplicates():
    merger = GoldenMasterMerger()
    row = FacitRow(section="6.1.2", name="Asbest", unit="kilogram")
    data = merger.merge_rows({}, [row, row])
    assert data["sections"]["6.1.2"]["tax_count"] == 1


def test_section_rule_engine_known_count():
    assert SectionRuleEngine().expected_count("6.1.2") == 103


def test_reference_rule_engine():
    assert ReferenceRuleEngine().is_reference("Toner färgpatron utan elektronik se farligt avfall")


def test_variant_rule_engine():
    assert VariantRuleEngine().find_variant("Avgift per container per dygn XX kr") == "Avgift per container per dygn"


def test_confidence_scoring():
    row = TaxRow(section="6.1.2", name="Asbest", unit="kilogram", ewc="170601*")
    assert ConfidenceScoring().score(row) > 0.8


def test_tax_pattern_matcher_best_match():
    row = TaxRow(name="Asbest, emballerat", unit="kilogram")
    facit = [{"name": "Asbest, emballerat", "unit": "kilogram", "variant": ""}]
    match, score = TaxPatternMatcher().best_match(row, facit)
    assert match is not None
    assert score > 0.9
