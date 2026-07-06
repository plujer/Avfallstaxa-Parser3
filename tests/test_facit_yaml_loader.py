from parser3.acceptance import FacitYamlLoader


def test_facit_yaml_loader_loads_612_rows():
    expectations = FacitYamlLoader().load("parser_facit.yaml")
    section = next(item for item in expectations if item.section == "6.1.2")

    assert section.expected_count == 103
    assert len(section.required_names) == 103
    assert "Avfall till energiåtervinning (240 L sopsäck)" in section.required_names
    assert "Spis, tvätt-, diskmaskin från verksamhet" in section.required_names
    assert "Toner, färgpatron utan elektronik – se farligt avfall" in section.ignored_names
