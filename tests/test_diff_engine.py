from parser3.diff import DiffEngine
from parser3.models import TaxRow

def test_diff_engine_detects_match_missing_extra():
    parsed = [TaxRow(section="6.1.2", name="Asbest", unit="kilogram"), TaxRow(section="6.1.2", name="Extra", unit="kilogram")]
    expected = [TaxRow(section="6.1.2", name="Asbest", unit="kilogram"), TaxRow(section="6.1.2", name="Missing", unit="kilogram")]
    result = DiffEngine().compare(parsed, expected)
    assert len(result.matched) == 1
    assert len(result.missing) == 1
    assert len(result.extra) == 1
    assert not result.passed
