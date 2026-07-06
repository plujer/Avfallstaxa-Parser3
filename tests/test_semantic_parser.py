from parser3.document import DocumentBlock
from parser3.semantic import SemanticParser, RowTypeClassifier, SectionTaxRules
from parser3.utils.constants import ROW_TYPE_REFERENCE

def test_row_type_classifier_reference():
    row_type, reason = RowTypeClassifier().classify(["Toner utan elektronik se farligt avfall"])
    assert row_type == ROW_TYPE_REFERENCE

def test_section_tax_rules_reference_not_exported():
    assert not SectionTaxRules().should_export("6.1.2", "Toner, färgpatron utan elektronik se farligt avfall")

def test_semantic_parser_assigns_section_to_tax_row():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="6.1.4 § Tillägg och avgifter"),
        DocumentBlock(order=1, kind="paragraph", text="Okänt farligt avfall XXX kr/fraktion"),
    ]
    result = SemanticParser().parse(blocks)
    assert len(result.tax_rows) == 1
    assert result.tax_rows[0].section == "6.1.4"
    assert result.tax_rows[0].chapter == "6"

def test_semantic_parser_keeps_reference_but_does_not_export():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="6.1.2 § Hanteringsavgifter"),
        DocumentBlock(order=1, kind="paragraph", text="Toner, färgpatron utan elektronik se farligt avfall"),
    ]
    result = SemanticParser().parse(blocks)
    assert len(result.tax_rows) == 0
    assert any(row.row_type == ROW_TYPE_REFERENCE for row in result.semantic_rows)
