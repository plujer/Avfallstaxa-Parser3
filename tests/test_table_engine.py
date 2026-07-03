from parser3.document import DocumentBlock
from parser3.rows import RowClassifier
from parser3.tables import CellNormalizer, SmartTableDetector
from parser3.utils.constants import ROW_TYPE_HEADER, ROW_TYPE_REFERENCE, ROW_TYPE_TAX


def test_cell_normalizer():
    n = CellNormalizer()
    assert n.normalize("  A\n B\xa0 ") == "A B"


def test_row_classifier_header():
    row = ["Typ av avfall", "EWC kod", "UN-nr", "Enhet", "Pris"]
    assert RowClassifier().classify(row).row_type == ROW_TYPE_HEADER


def test_row_classifier_tax():
    row = ["Asbest, emballerat", "170601*", "2212", "kilogram", "22,88"]
    assert RowClassifier().classify(row).row_type == ROW_TYPE_TAX


def test_row_classifier_reference():
    row = ["Toner, färgpatron utan elektronik", "080307*", "", "se farligt avfall"]
    assert RowClassifier().classify(row).row_type == ROW_TYPE_REFERENCE


def test_smart_table_detector_visual_rows():
    blocks = [
        DocumentBlock(order=0, kind="paragraph", text="Rubrik"),
        DocumentBlock(order=1, kind="paragraph", text="Fakturaavgift XX kr"),
        DocumentBlock(order=2, kind="paragraph", text="Akutsäck XX kr"),
    ]
    tables = SmartTableDetector().detect(blocks)
    assert len(tables) == 1
    assert tables[0].source == "visual"
