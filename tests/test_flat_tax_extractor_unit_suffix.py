from parser3.extractors import FlatTaxExtractor


def test_flat_extractor_splits_fraktion_suffix_from_name():
    rows = FlatTaxExtractor().extract_line("Ej redovisad eller fel redovisad fraktion av avfall XXXX kr/fraktion", chapter="6", section="6.1.1")

    assert len(rows) == 1
    assert rows[0].name == "Ej redovisad eller fel redovisad fraktion av avfall"
    assert rows[0].unit == "fraktion"


def test_flat_extractor_splits_besok_suffix_from_name():
    rows = FlatTaxExtractor().extract_line("Verksamheter XX kr/besök", chapter="6", section="6.1.1")

    assert len(rows) == 1
    assert rows[0].name == "Verksamheter"
    assert rows[0].unit == "besök"
