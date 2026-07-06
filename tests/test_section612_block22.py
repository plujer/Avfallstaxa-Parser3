from parser3.extractors import Section612Extractor


def test_section612_extracts_multiplication_star_variant():
    rows = Section612Extractor().extract_line(
        "Skrymmande avfall till energiåtervinning större än 20*20*80 kilogram",
        chapter="6",
        section="6.1.2",
    )
    assert len(rows) == 1
    assert rows[0].name == "Skrymmande avfall till energiåtervinning större än 20×20×80"


def test_section612_extracts_remaining_block_a_rows():
    extractor = Section612Extractor()
    for text, expected in [
        ("Isolering utan innehåll av asbest m3", "Isolering utan innehåll av asbest"),
        ("WC-stol kilogram", "WC-stol"),
        ("Stubbar rötter för krossning kilogram", "Stubbar/rötter för krossning"),
    ]:
        rows = extractor.extract_line(text, chapter="6", section="6.1.2")
        assert len(rows) == 1
        assert rows[0].name == expected
