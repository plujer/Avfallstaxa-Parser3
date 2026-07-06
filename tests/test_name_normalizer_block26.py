from parser3.acceptance.name_normalizer import NameNormalizer


def test_normalizer_removes_ewc_with_star_before_symbol_normalization():
    norm = NameNormalizer()
    assert norm.normalize("Isolering utan innehåll av asbest 170601* kilogram") == "isolering utan innehåll av asbest"


def test_normalizer_keeps_multiplication_dimension_after_fix():
    norm = NameNormalizer()
    assert norm.normalize("större än 20*20*80") == "större än 20x20x80"
