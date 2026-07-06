from parser3.acceptance import FacitYamlLoader


def test_facit_yaml_loader_loads_611_rows():
    expectations = FacitYamlLoader().load("parser_facit.yaml")
    section = next(item for item in expectations if item.section == "6.1.1")

    assert section.expected_count == 6
    assert len(section.required_names) == 6
    assert "Verksamheter" in section.required_names
    assert "Ej redovisad ankomst till ÅVC (för företagare och privatpersoner som lämnar verksamhetsavfall utan att anmäla sin ankomst)" in section.required_names
