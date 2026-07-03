from parser3.extractors import TaxRowExtractor, MetadataExtractor
from parser3.taxonomy import UnitDetector


def test_unit_detector_detects_kr_per_fraktion():
    assert UnitDetector().detect(["Okänt farligt avfall XXX kr/fraktion"]) == "fraktion"


def test_metadata_extractor_ewc_and_un():
    extractor = MetadataExtractor()
    cells = ["Asbest, emballerat", "170601*", "2212", "kilogram", "22,88"]
    assert extractor.extract_ewc(cells) == "170601*"
    assert extractor.extract_un(cells) == "2212"


def test_metadata_extractor_ewc_without_star():
    extractor = MetadataExtractor()
    cells = ["Avfall till energiåtervinning", "200301", "", "kilogram", ""]
    assert extractor.extract_ewc(cells) == "200301"


def test_tax_row_extractor_extracts_row():
    rows = [
        ["Typ av avfall", "EWC kod", "UN-nr", "Enhet", "Pris"],
        ["Asbest, emballerat", "170601*", "2212", "kilogram", "22,88"],
        ["Toner, färgpatron utan elektronik", "080307*", "", "se farligt avfall"],
    ]
    extracted = TaxRowExtractor().extract_from_rows(rows, chapter="6", section="6.1.2", group="Farligt avfall")
    assert len(extracted) == 1
    assert extracted[0].name == "Asbest, emballerat"
    assert extracted[0].ewc == "170601*"
    assert extracted[0].un_number == "2212"
