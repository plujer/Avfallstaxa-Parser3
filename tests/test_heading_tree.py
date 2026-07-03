from parser3.document import DocumentBlock
from parser3.headings import HeadingTreeBuilder, SectionClassifier


def test_section_classifier_detects_numbered_heading():
    match = SectionClassifier().classify("6.1.2 § Hanteringsavgifter för avfall")
    assert match is not None
    assert match.number == "6.1.2"
    assert match.level == 3
    assert match.title == "Hanteringsavgifter för avfall"


def test_heading_tree_builder_creates_hierarchy():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="2 § Avgifter och tjänster"),
        DocumentBlock(order=1, kind="paragraph", text="2.2 § Årlig hämtningsavgift"),
        DocumentBlock(order=2, kind="paragraph", text="2.2.4 § Flerbostadshus"),
        DocumentBlock(order=3, kind="paragraph", text="6 § Avfall inlämnat på återvinningscentral"),
        DocumentBlock(order=4, kind="paragraph", text="6.1.2 § Hanteringsavgifter"),
    ]

    roots = HeadingTreeBuilder().build(blocks)

    assert len(roots) == 2
    assert roots[0].number == "2"
    assert roots[0].children[0].number == "2.2"
    assert roots[0].children[0].children[0].number == "2.2.4"
    assert roots[1].children[0].number == "6.1.2"
