from parser3.rows import RowClassifier
from parser3.semantic import SectionTaxRules
from parser3.utils.constants import ROW_TYPE_INFO, ROW_TYPE_TAX


def test_definition_text_with_unit_word_is_not_tax():
    row = ["Abonnemang innebär regelbunden tömning med bestämt intervall."]
    assert RowClassifier().classify(row).row_type == ROW_TYPE_INFO


def test_long_legal_text_with_avgift_is_not_tax():
    row = ["Dessa föreskrifter om avgifter har kommunen beslutat med stöd av 27 kap. 4 § miljöbalken."]
    assert RowClassifier().classify(row).row_type == ROW_TYPE_INFO


def test_price_placeholder_is_tax():
    row = ["Fakturavgift XX kr"]
    assert RowClassifier().classify(row).row_type == ROW_TYPE_TAX


def test_numeric_decimal_price_is_tax():
    row = ["Asbest", "170601*", "2212", "kilogram", "22,88"]
    assert RowClassifier().classify(row).row_type == ROW_TYPE_TAX


def test_chapter_1_never_exports():
    assert not SectionTaxRules().should_export("1.3", "Fakturavgift XX kr")


def test_real_tax_section_exports():
    assert SectionTaxRules().should_export("6.1.4", "Okänt farligt avfall XXX kr/fraktion")
