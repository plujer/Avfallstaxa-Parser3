from parser3.extractors import FlatTaxExtractor


def test_flat_extractor_removes_single_price_from_name():
    rows = FlatTaxExtractor().extract_line("Fritidshus XX kr", chapter="2", section="2.1")
    assert len(rows) == 1
    assert rows[0].name == "Fritidshus"
    assert rows[0].price == "XX kr"


def test_flat_extractor_creates_multiple_price_rows():
    rows = FlatTaxExtractor().extract_line("Kärl 240 l (mat-/restavfall) XX kr XX kr XX kr", chapter="2", section="2.2.4")
    assert len(rows) == 3
    assert all(row.name == "Kärl 240 l (mat-/restavfall)" for row in rows)


def test_flat_extractor_skips_lowercase_continuation_fragment():
    rows = FlatTaxExtractor().extract_line("av avfall under kommunalt ansvar. XX kr", chapter="2", section="2.1")
    assert rows == []


def test_flat_extractor_skips_tillkommer_note():
    rows = FlatTaxExtractor().extract_line("Vid tömning två (2) gånger per vecka tillkommer XXX kr eller %.", chapter="2", section="2.2.4")
    assert rows == []
