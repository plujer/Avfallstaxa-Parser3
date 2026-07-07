from excel_builder.variant_intelligence import VariantMatcher


def test_variant_matcher_accepts_same_family_same_interval():
    comparison = VariantMatcher().compare_codes("KÄ240RM26", "KÄ240RM26")
    assert comparison.same_family is True
    assert comparison.same_variant is True
    assert comparison.score == 1.0


def test_variant_matcher_flags_interval_difference_inside_family():
    comparison = VariantMatcher().compare_codes("KÄ240RM26", "KÄ240RM52")
    assert comparison.same_family is True
    assert comparison.same_variant is False
    assert "interval" in comparison.mismatched_fields


def test_variant_matcher_does_not_match_different_family_as_variant():
    comparison = VariantMatcher().compare_codes("KÄ240RM26", "KÄ190RE26")
    assert comparison.same_family is False
    assert comparison.same_variant is False
    assert comparison.score < 0.5


def test_variant_bonus_rewards_exact_variant_more_than_family_only():
    matcher = VariantMatcher()
    assert matcher.bonus("KÄ240RM26", "KÄ240RM26") > matcher.bonus("KÄ240RM26", "KÄ240RM52")
