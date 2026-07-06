from parser3.acceptance.name_normalizer import NameNormalizer


def test_name_normalizer_does_not_remove_four_digit_measurements():
    norm = NameNormalizer()
    text = "Skrymmande avfall till energiåtervinning större än 20*20*80"
    assert norm.normalize(text) == "skrymmande avfall till energiåtervinning större än 20x20x80"


def test_name_normalizer_removes_ewc_but_not_product_number_text():
    norm = NameNormalizer()
    assert norm.normalize("Betong, lättbetong 170101 kilogram") == "betong, lättbetong"
