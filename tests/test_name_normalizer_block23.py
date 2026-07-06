from parser3.acceptance.name_normalizer import NameNormalizer


def test_normalizer_collapses_duplicated_name_after_metadata_removal():
    norm = NameNormalizer()
    text = (
        "Skrymmande avfall till energiåtervinning större än 20*20*80 "
        "Skrymmande avfall till energiåtervinning större än 20*20*80 "
        "200307 200307 kilogram kilogram"
    )
    assert norm.normalize(text) == "skrymmande avfall till energiåtervinning större än 20x20x80"


def test_normalizer_does_not_damage_single_name():
    norm = NameNormalizer()
    assert norm.normalize("Avfall till energiåtervinning") == "avfall till energiåtervinning"


def test_normalizer_removes_duplicate_with_units_between_end():
    norm = NameNormalizer()
    text = "WC-stol WC-stol kilogram kilogram"
    assert norm.normalize(text) == "wc-stol"
