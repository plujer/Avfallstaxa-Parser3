from parser3.context import ContextEngine, SectionContextAssigner
from parser3.document import DocumentBlock


def test_context_assigner_keeps_section_active():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="6.1.4 § Tillägg och avgifter"),
        DocumentBlock(order=1, kind="paragraph", text="Okänt farligt avfall XXX kr/fraktion"),
        DocumentBlock(order=2, kind="paragraph", text="Ombud för rapportering XXX kr/tillfälle"),
    ]
    assigned = SectionContextAssigner().assign(blocks)
    assert assigned[1].context.section == "6.1.4"
    assert assigned[2].context.section == "6.1.4"


def test_context_engine_summary():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="6.1.2 § Hanteringsavgifter"),
        DocumentBlock(order=1, kind="paragraph", text="Asbest, emballerat 170601* 2212 kilogram 22,88"),
        DocumentBlock(order=2, kind="paragraph", text="6.1.4 § Tillägg och avgifter"),
        DocumentBlock(order=3, kind="paragraph", text="Okänt farligt avfall XXX kr/fraktion"),
    ]
    summary = ContextEngine().summary(blocks)
    assert summary.section_counts["6.1.2"] == 2
    assert summary.section_counts["6.1.4"] == 2


def test_table_row_context_inherits_section():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="6.1.2 § Hanteringsavgifter"),
        DocumentBlock(order=1, kind="table", text="", rows=[
            ["Typ av avfall", "EWC kod", "UN-nr", "Enhet", "Pris"],
            ["Asbest", "170601*", "2212", "kilogram", "22,88"],
        ]),
    ]
    assigned = SectionContextAssigner().assign(blocks)
    table_block = assigned[1]
    assert table_block.row_contexts[0].section == "6.1.2"
    assert table_block.row_contexts[1].section == "6.1.2"
