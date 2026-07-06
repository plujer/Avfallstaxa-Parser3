from parser3.document import HeadingNumberer


def test_heading_numberer_generates_section_numbers():
    numberer = HeadingNumberer()

    h1, meta1 = numberer.prefix_heading("Allmänna bestämmelser", "Heading 1")
    h2, meta2 = numberer.prefix_heading("Allmänt", "Heading 2")
    h3, meta3 = numberer.prefix_heading("Reservavgift", "Heading 3")

    assert h1 == "1 § Allmänna bestämmelser"
    assert h2 == "1.1 § Allmänt"
    assert h3 == "1.1.1 § Reservavgift"
    assert meta1["section_number"] == "1"
    assert meta2["section_number"] == "1.1"


def test_heading_numberer_increments_siblings():
    numberer = HeadingNumberer()

    assert numberer.prefix_heading("Kapitel", "Heading 1")[0] == "1 § Kapitel"
    assert numberer.prefix_heading("A", "Heading 2")[0] == "1.1 § A"
    assert numberer.prefix_heading("B", "Heading 2")[0] == "1.2 § B"
    assert numberer.prefix_heading("Nytt kapitel", "Heading 1")[0] == "2 § Nytt kapitel"


def test_heading_numberer_does_not_double_prefix():
    numberer = HeadingNumberer()
    text, meta = numberer.prefix_heading("2.1 § Grundavgift", "Heading 2")
    assert text == "2.1 § Grundavgift"
