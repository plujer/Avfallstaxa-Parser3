from excel_builder.semantic_attributes import SemanticAttributeExtractor


def test_semantic_attribute_extractor_detects_material_unit_and_container():
    profile = SemanticAttributeExtractor().extract(
        tax_code="ASB1",
        text="Asbest i säck debiteras kr/kg vid besök",
        source="TEST",
    )

    assert "ASBEST" in profile.materials
    assert "SÄCK" in profile.container_types
    assert "KG" in profile.units
    assert "BESÖK" in profile.units
    assert profile.attribute_count >= 4


def test_semantic_attribute_extractor_detects_property_and_interval():
    profile = SemanticAttributeExtractor().extract(
        tax_code="KÄ240RM26",
        text="Kärl 240 liter rest-/matavfall en- och tvåbostadshus 26 dagar",
        source="TEST",
    )

    assert "KÄRL" in profile.container_types
    assert "REST/MAT" in profile.waste_types
    assert "SMÅHUS" in profile.property_types
    assert "26 DAGAR" in profile.intervals
