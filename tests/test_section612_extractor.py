from parser3.extractors import Section612Extractor


def test_section612_extractor_extracts_block_a_without_price():
    rows = Section612Extractor().extract_line(
        "Betong, lättbetong kilogram",
        chapter="6",
        section="6.1.2",
    )
    assert len(rows) == 1
    assert rows[0].name == "Betong, lättbetong"


def test_section612_extractor_ignores_reference():
    rows = Section612Extractor().extract_line(
        "Toner, färgpatron utan elektronik – se farligt avfall",
        chapter="6",
        section="6.1.2",
    )
    assert rows == []
