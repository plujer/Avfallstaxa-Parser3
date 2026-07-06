from parser3.acceptance import FacitYamlLoader


def test_facit_yaml_loader_loads_613_rows():
    expectations = FacitYamlLoader().load("parser_facit.yaml")
    section = next(item for item in expectations if item.section == "6.1.3")

    assert section.expected_count == 4
    assert len(section.required_names) == 4
    assert section.required_names.count("Container X m³") == 3
    assert "Omklassning av felsorterad container" in section.required_names
