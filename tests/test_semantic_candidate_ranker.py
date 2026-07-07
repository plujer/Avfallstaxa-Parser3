from excel_builder.models import TaxSemanticProfile, TaxSemanticProfileKey
from excel_builder.semantic import SemanticCandidateRanker


def profile(source, source_id, **kwargs):
    return TaxSemanticProfile(
        source=source,
        source_id=source_id,
        key=TaxSemanticProfileKey(**kwargs),
        tax_code=kwargs.get("tax_code", ""),
    )


def test_semantic_candidate_ranker_scores_and_explains_candidate():
    word = profile(
        "WORD",
        "WORD:1",
        category="Hushåll",
        waste_type="Restavfall",
        container_type="Kärl",
        container_volume_liter="190",
        factor_hint="VOLYM/BEHÅLLARE",
    )
    standard = profile(
        "STANDARD",
        "Standard:2",
        category="Hushåll",
        waste_type="Restavfall",
        container_type="Kärl",
        container_volume_liter="190",
        factor_hint="VOLYM/BEHÅLLARE",
    )

    report = SemanticCandidateRanker().rank([word], [standard])

    assert report.total_candidates == 1
    assert report.candidates[0].score >= 0.70
    assert report.candidates[0].status in {"REVIEW_REQUIRED", "STANDARD_PROPOSAL"}
    assert "Matchar" in report.candidates[0].explanation


def test_semantic_candidate_ranker_returns_top_n():
    word = profile("WORD", "WORD:1", waste_type="Restavfall")
    candidates = [
        profile("STANDARD", f"STD:{idx}", waste_type="Restavfall")
        for idx in range(20)
    ]

    report = SemanticCandidateRanker().rank([word], candidates, top_n=5)

    assert report.total_candidates == 5
    assert report.unique_word_profiles == 1
