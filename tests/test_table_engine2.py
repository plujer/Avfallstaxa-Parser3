from parser3.tables2 import PriceCellDetector, StructuredTaxExtractor


def test_price_cell_detector():
    detector = PriceCellDetector()
    assert detector.is_price_cell("XX kr")
    assert detector.is_price_cell("1 650,00 kr")
    assert not detector.is_price_cell("Kärl 240 l XX kr")


def test_structured_extractor_splits_three_prices_into_variants():
    rows = [
        ["Typ av behållare", "Hämtning varje vecka", "Hämtning var 14:e dag", "Hämtning månadsvis"],
        ["Kärl 240 l (mat-/restavfall)", "XX kr", "XX kr", "XX kr"],
    ]
    extracted = StructuredTaxExtractor().extract_table(rows, chapter="2", section="2.2.4")
    assert len(extracted) == 3
    assert all(row.name == "Kärl 240 l (mat-/restavfall)" for row in extracted)
    assert extracted[0].variant == "Hämtning varje vecka"
    assert extracted[1].variant == "Hämtning var 14:e dag"
    assert extracted[2].variant == "Hämtning månadsvis"


def test_structured_extractor_keeps_name_separate_from_price():
    rows = [
        ["Abonnemangstyp", "Grundavgift per år"],
        ["Fritidshus", "XX kr"],
    ]
    extracted = StructuredTaxExtractor().extract_table(rows, chapter="2", section="2.1")
    assert len(extracted) == 1
    assert extracted[0].name == "Fritidshus"
    assert extracted[0].price == "XX kr"
