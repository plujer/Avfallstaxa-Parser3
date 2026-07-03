from parser3.document import DocumentBlock, PageIterator, StyleReader


def test_style_reader_detects_heading():
    reader = StyleReader()
    assert reader.is_heading("Heading 1")
    assert reader.heading_level("Heading 3") == 3
    assert not reader.is_heading("Body Text")


def test_page_iterator_groups_blocks():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="A", metadata={"page": 1}),
        DocumentBlock(order=1, kind="paragraph", text="B", metadata={"page": 1}),
        DocumentBlock(order=2, kind="paragraph", text="C", metadata={"page": 2}),
    ]
    grouped = PageIterator().group_by_page(blocks)
    assert len(grouped[1]) == 2
    assert len(grouped[2]) == 1
