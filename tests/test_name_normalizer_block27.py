from parser3.acceptance.name_normalizer import NameNormalizer


def test_normalizer_removes_ewc_code_with_star_without_leaving_x():
    norm = NameNormalizer()
    assert norm.normalize("Isolering utan innehåll av asbest 170601* kilogram") == "isolering utan innehåll av asbest"


def test_normalizer_removes_duplicated_ewc_code_with_star_without_leaving_x():
    norm = NameNormalizer()
    text = "Isolering utan innehåll av asbest Isolering utan innehåll av asbest 170601* 170601* kilogram kilogram"
    assert norm.normalize(text) == "isolering utan innehåll av asbest"


def test_normalizer_keeps_dimension_star_as_x():
    norm = NameNormalizer()
    assert norm.normalize("större än 20*20*80") == "större än 20x20x80"
