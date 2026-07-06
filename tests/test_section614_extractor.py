from parser3.extractors import Section614Extractor


def test_section614_extracts_split_elkretsen_row():
    previous = "Ombud för registrering av El-kretsen avlämnarintyg"
    current = "i Hämtplatsportalen XXX kr/tillfälle"

    rows = Section614Extractor().extract_combined(previous, current, chapter="6", section="6.1.4")

    assert len(rows) == 1
    assert rows[0].name == "Ombud för registrering av El-kretsen avlämnarintyg i Hämtplatsportalen"
    assert rows[0].unit == "tillfälle"
    assert rows[0].price == "XXX kr"
