from excel_builder.models import TaxSemanticProfile, TaxSemanticProfileKey
from excel_builder.semantic.semantic_candidate_ranker import SemanticCandidateRanker
from excel_builder.tax_family import TaxFamilyMatcher, TaxFamilyRepository


def test_tax_family_matcher_detects_same_family_different_interval():
    match = TaxFamilyMatcher().compare("KÄ240RM26", "KÄ240RM52")

    assert match.same_family is True
    assert match.same_variant is False
    assert match.word_family == "KÄ240RM"
    assert match.candidate_family == "KÄ240RM"


def test_tax_family_repository_groups_members():
    report = TaxFamilyRepository().from_codes(["KÄ240RM26", "KÄ240RM52", "KÄ240RMFV", "KÄ190RE26"])

    family = report.family("KÄ240RM")

    assert report.total_families == 2
    assert family is not None
    assert family.member_count == 3
    assert family.intervals == ["26", "52"]
    assert family.variants == ["FV"]


def test_semantic_candidate_ranker_adds_tax_family_bonus():
    key = TaxSemanticProfileKey(category="karl", waste_type="rest-mat", container_type="Kärl")
    word = TaxSemanticProfile(source="WORD", source_id="w1", key=key, tax_code="KÄ240RM26")
    candidate = TaxSemanticProfile(source="STANDARD", source_id="s1", key=key, tax_code="KÄ240RM52")

    score, parts = SemanticCandidateRanker().score(word, candidate)

    assert score > 0.0
    assert any(part.field == "tax_family" and part.score > 0 for part in parts)
