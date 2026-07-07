from excel_builder.composite_matching import CompositeMatcher
from excel_builder.models import CompositeMatchInput


def test_composite_matcher_combines_edp_family_variant_and_attributes():
    matcher = CompositeMatcher()
    result = matcher.compare(
        CompositeMatchInput(
            word_tax_code="KÄ240RM26",
            candidate_tax_code="KÄ240RM26",
            word_text="240 liter restavfall kärl hämtning 26 gånger per år",
            candidate_text="Kärl 240 liter restavfall 26 ggr per år",
            edp_exact_match=True,
            same_context=True,
            same_structure=True,
        )
    )

    assert result.status == "MATCH"
    assert result.score >= 0.80
    assert {part.name for part in result.parts} >= {
        "edp_exact",
        "tax_family",
        "variant",
        "semantic_attributes",
        "hierarchical_context",
        "document_structure",
    }


def test_composite_matcher_marks_weak_match_for_review_or_no_match():
    matcher = CompositeMatcher()
    result = matcher.compare(
        CompositeMatchInput(
            word_tax_code="KÄ240RM26",
            candidate_tax_code="SLAM104",
            word_text="240 liter restavfall kärl",
            candidate_text="Slamtömning brunn",
        )
    )

    assert result.status in {"REVIEW", "NO_MATCH"}
    assert result.score < 0.65
