from excel_builder.variant_intelligence import VariantParser


def test_variant_parser_reads_code_dimensions():
    profile = VariantParser().parse("KÄ240RM26")
    assert profile.family_code == "KÄ240RM"
    assert profile.volume_liter == "240"
    assert profile.waste_code == "RM"
    assert profile.interval == "26"
    assert profile.variant_key == "240|RM|26"


def test_variant_parser_reads_fritid_variant_from_code():
    profile = VariantParser().parse("KÄ240RMFV")
    assert profile.family_code == "KÄ240RM"
    assert profile.variant == "FV"
    assert profile.usage_type == "FRITID"


def test_variant_parser_uses_text_when_code_is_incomplete():
    profile = VariantParser().parse("KÄ", "240 liter restavfall permanent")
    assert profile.volume_liter == "240"
    assert profile.waste_code == "RE"
    assert profile.usage_type == "PERMANENT"
