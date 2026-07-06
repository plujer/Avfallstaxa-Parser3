from parser3.acceptance import FacitYamlLoader


def test_facit_yaml_loader_loads_614_rows():
    expectations = FacitYamlLoader().load("parser_facit.yaml")
    section = next(item for item in expectations if item.section == "6.1.4")

    assert section.expected_count == 4
    assert len(section.required_names) == 4
    assert "Ombud för registrering av El-kretsen avlämnarintyg i Hämtplatsportalen" in section.required_names
