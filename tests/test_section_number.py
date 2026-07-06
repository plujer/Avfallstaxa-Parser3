from parser3.sections import SectionNumber, SectionFilter


def test_section_number_parts():
    number = SectionNumber("6.1.2")
    assert number.parts == [6, 1, 2]
    assert number.level == 3
    assert number.chapter == "6"


def test_section_number_child():
    assert SectionNumber("6.1.2").is_child_of(SectionNumber("6.1"))


def test_section_filter_false_heading():
    assert SectionFilter().is_probably_false_heading("Förslag till taxestruktur 2026-03-13")
