from parser3.extractors import Section611Extractor


def test_section611_extracts_split_ej_redovisad_ankomst_row():
    previous = "Ej redovisad ankomst till ÅVC (för företagare och privatpersoner"
    current = "som lämnar verksamhetsavfall utan att anmäla sin ankomst) XX kr/besök"

    rows = Section611Extractor().extract_combined(previous, current, chapter="6", section="6.1.1")

    assert len(rows) == 1
    assert rows[0].name == (
        "Ej redovisad ankomst till ÅVC (för företagare och privatpersoner "
        "som lämnar verksamhetsavfall utan att anmäla sin ankomst)"
    )
    assert rows[0].unit == "besök"
    assert rows[0].price == "XX kr"
