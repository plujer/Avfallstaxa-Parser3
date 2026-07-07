from excel_builder.taxcode import TaxCodeParser


def test_tax_code_parser_parses_kar_240_rm_26_fv():
    parsed = TaxCodeParser().parse("KÄ240RM26FV")

    assert parsed.prefix == "KÄ"
    assert parsed.container_type == "Kärl"
    assert parsed.volume_liter == "240"
    assert parsed.waste_code == "RM"
    assert parsed.interval == "26"
    assert parsed.variant == "FV"
    assert parsed.family_key == "KÄ240RM"


def test_tax_code_parser_parses_standard_restavfall_code():
    parsed = TaxCodeParser().parse("KÄ190RE156")

    assert parsed.volume_liter == "190"
    assert parsed.waste_code == "RE"
    assert parsed.waste_type == "Restavfall"
    assert parsed.interval == "156"


def test_tax_code_parser_keeps_unknown_suffix():
    parsed = TaxCodeParser().parse("XYZ123ABC")

    assert parsed.suffix or parsed.notes
