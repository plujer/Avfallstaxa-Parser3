from excel_builder.matching import MatchNormalizer


def test_match_normalizer_removes_section_symbol():
    normalizer = MatchNormalizer()

    assert normalizer.normalize_section("§2.1") == "2.1"
    assert normalizer.normalize_section("§ 6.1.2") == "6.1.2"
    assert normalizer.normalize_section("6.1.2") == "6.1.2"


def test_match_normalizer_row_key_matches_section_symbol_variants():
    normalizer = MatchNormalizer()

    parser_key = normalizer.row_key("6.1.2", "Asbest, emballerat", "", "kilogram")
    excel_key = normalizer.row_key("§6.1.2", "Asbest, emballerat", "", "kilogram")

    assert parser_key == excel_key


def test_match_normalizer_weak_key_matches_section_symbol_variants():
    normalizer = MatchNormalizer()

    parser_key = normalizer.weak_key("2.1", "Fritidshus")
    excel_key = normalizer.weak_key("§2.1", "Fritidshus")

    assert parser_key == excel_key
