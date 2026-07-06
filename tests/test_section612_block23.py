from parser3.extractors import Section612Extractor


def test_section612_extracts_duplicated_skrtymmande_word_row():
    text = (
        "Skrymmande avfall till energiåtervinning större än 20*20*80 "
        "Skrymmande avfall till energiåtervinning större än 20*20*80 "
        "200307 200307 kilogram kilogram"
    )
    rows = Section612Extractor().extract_line(text, chapter="6", section="6.1.2")
    assert len(rows) == 1
    assert rows[0].name == "Skrymmande avfall till energiåtervinning större än 20×20×80"
