from parser3.acceptance import MissingRowDiagnostics
from parser3.models import TaxRow
from parser3.semantic import SemanticRow


def test_missing_row_diagnostics_finds_semantic_candidate():
    tax_rows = [TaxRow(section="6.1.2", name="Betong, lättbetong")]
    semantic_rows = [
        SemanticRow(
            section="6.1.2",
            text="WC-stol kilogram",
            row_type="info",
            reason="default info",
            order=10,
        )
    ]

    result = MissingRowDiagnostics().run(tax_rows, semantic_rows)

    expected_names = [item.expected_name for item in result.diagnostics]
    assert "WC-stol" in expected_names
    wc = next(item for item in result.diagnostics if item.expected_name == "WC-stol")
    assert wc.exact_semantic_hits or wc.fuzzy_semantic_hits or wc.nearby_semantic_rows
