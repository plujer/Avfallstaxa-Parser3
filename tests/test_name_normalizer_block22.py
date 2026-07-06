from parser3.acceptance.name_normalizer import NameNormalizer


def test_normalizer_treats_multiplication_symbols_same():
    norm = NameNormalizer()
    assert norm.normalize("20×20×80") == norm.normalize("20*20*80")


def test_normalizer_removes_metadata_and_units():
    norm = NameNormalizer()
    assert norm.normalize("Isolering utan innehåll av asbest 170601* kilogram") == "isolering utan innehåll av asbest"
    assert norm.normalize("WC-stol kilogram") == "wc-stol"


def test_normalizer_aliases_stubbar_roetter():
    norm = NameNormalizer()
    assert norm.normalize("Stubbar rötter för krossning kilogram") == norm.normalize("Stubbar/rötter för krossning")


def test_normalizer_keeps_full_long_name():
    norm = NameNormalizer()
    assert norm.normalize("Skrymmande avfall till energiåtervinning större än 20*20*80 kilogram") == (
        "skrymmande avfall till energiåtervinning större än 20x20x80"
    )
