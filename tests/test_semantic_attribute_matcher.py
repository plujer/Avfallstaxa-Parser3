from excel_builder.models import SemanticAttributeProfile
from excel_builder.semantic_attributes import SemanticAttributeMatcher


def test_semantic_attribute_matcher_scores_shared_attributes():
    word = SemanticAttributeProfile(materials=("ASBEST",), units=("KG",), container_types=("SÄCK",))
    candidate = SemanticAttributeProfile(materials=("ASBEST",), units=("KG",), container_types=("CONTAINER",))

    comparison = SemanticAttributeMatcher().compare(word, candidate)

    assert comparison.score > 0.5
    assert "materials:ASBEST" in comparison.matched_attributes
    assert "units:KG" in comparison.matched_attributes
    assert "container_types" in comparison.missing_attributes
