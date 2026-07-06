from parser3.headings import SectionClassifier


def test_accepts_real_section_with_paragraph_symbol():
    match = SectionClassifier().classify("6.1.2 § Hanteringsavgifter för avfall inlämnat på återvinningscentral")
    assert match is not None
    assert match.number == "6.1.2"


def test_accepts_main_chapter():
    match = SectionClassifier().classify("2 § Avgifter och tjänster")
    assert match is not None
    assert match.number == "2"


def test_rejects_year():
    assert SectionClassifier().classify("2026") is None


def test_rejects_date():
    assert SectionClassifier().classify("2026-03-13") is None


def test_rejects_ewc_code():
    assert SectionClassifier().classify("170601*") is None
    assert SectionClassifier().classify("200301") is None


def test_rejects_un_number():
    assert SectionClassifier().classify("3295") is None


def test_rejects_price_row():
    assert SectionClassifier().classify("Okänt farligt avfall XXX kr/fraktion") is None


def test_rejects_tax_data_row_starting_with_container():
    assert SectionClassifier().classify("Container X m3 XX kr") is None


def test_rejects_document_title_with_year():
    assert SectionClassifier().classify("Förslag till taxestruktur för Avfallssamverkan Norr 2026-03-13") is None
