from parser3.models import TaxRow
from parser3.validation import DuplicateDetector, MissingTaxDetector, ValidationEngine


def test_duplicate_detector_finds_duplicate():
    rows = [
        TaxRow(section="6.1.2", name="Asbest", unit="kilogram"),
        TaxRow(section="6.1.2", name="Asbest", unit="kilogram"),
    ]
    duplicates = DuplicateDetector().find_duplicates(rows)
    assert len(duplicates) == 1


def test_missing_tax_detector_finds_missing_section():
    rows = [TaxRow(section="", name="Asbest", unit="kilogram")]
    invalid = MissingTaxDetector().find_invalid_rows(rows)
    assert invalid


def test_validation_engine_passes_valid_rows_without_golden():
    rows = [TaxRow(section="6.1.2", name="Asbest", unit="kilogram")]
    result = ValidationEngine().validate(rows)
    assert result.passed
