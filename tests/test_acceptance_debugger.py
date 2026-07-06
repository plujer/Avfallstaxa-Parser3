from parser3.acceptance import AcceptanceDebugger
from parser3.models import TaxRow
from parser3.semantic import SemanticRow


def test_acceptance_debugger_reports_missing_from_catalog():
    rows = [TaxRow(section="6.1.2", name="Asbest, emballerat")]
    semantic = [
        SemanticRow(
            row_type="info",
            text="Smittförande avfall 180103* 3291 kilogram 40,31",
            section="6.1.2",
            reason="test",
        )
    ]

    result = AcceptanceDebugger().debug(rows, semantic)
    section = result.sections[0]

    assert section.section == "6.1.2"
    assert "Smittförande avfall" in section.missing_names
    assert section.non_tax_candidates


def test_acceptance_debugger_possible_matches():
    rows = [TaxRow(section="6.1.2", name="Rökdetektor Am 241")]
    semantic = []

    result = AcceptanceDebugger().debug(rows, semantic)
    section = result.sections[0]

    assert "Rökdetektor med Am 241" in section.missing_names
    assert section.possible_matches["Rökdetektor med Am 241"]
