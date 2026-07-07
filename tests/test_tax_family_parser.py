from excel_builder.tax_family import TaxFamilyParser


def test_tax_family_parser_groups_intervals_under_base_family():
    parser = TaxFamilyParser()

    member_26 = parser.parse_member("KÄ240RM26")
    member_52 = parser.parse_member("KÄ240RM52")
    member_fv = parser.parse_member("KÄ240RMFV")

    assert member_26.family_key.value == "KÄ240RM"
    assert member_52.family_key.value == "KÄ240RM"
    assert member_fv.family_key.value == "KÄ240RM"
    assert member_26.interval == "26"
    assert member_52.interval == "52"
    assert member_fv.variant == "FV"


def test_tax_family_parser_keeps_different_waste_codes_apart():
    parser = TaxFamilyParser()

    rest = parser.parse_member("KÄ190RE26")
    mat = parser.parse_member("KÄ140MA26")

    assert rest.family_key.value == "KÄ190RE"
    assert mat.family_key.value == "KÄ140MA"
    assert rest.family_key.value != mat.family_key.value
