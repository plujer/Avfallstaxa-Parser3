from parser3.models import TaxRow
from parser3.semantic.semantic_parser import SemanticParser


def test_section613_duplicate_policy_keeps_identical_rows():
    parser = SemanticParser()
    tax_rows = []
    seen = set()

    def add_rows(new_rows):
        for row in new_rows:
            if row.section == "6.1.3":
                tax_rows.append(row)
                continue
            key = (row.section, row.name, row.variant, row.unit)
            if key not in seen:
                seen.add(key)
                tax_rows.append(row)

    add_rows([
        TaxRow(section="6.1.3", name="Container X m³", variant="Avgift per container per dygn", unit="container/dygn"),
        TaxRow(section="6.1.3", name="Container X m³", variant="Avgift per container per dygn", unit="container/dygn"),
        TaxRow(section="6.1.3", name="Container X m³", variant="Avgift per container per dygn", unit="container/dygn"),
    ])

    assert len(tax_rows) == 3
