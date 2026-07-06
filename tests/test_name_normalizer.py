from parser3.acceptance import AcceptanceRunner
from parser3.acceptance.name_normalizer import NameNormalizer
from parser3.acceptance.acceptance_models import AcceptanceExpectation
from parser3.models import TaxRow


def test_name_normalizer_aliases_common_612_spellings():
    norm = NameNormalizer()
    assert norm.normalize("Flourvätesyra") == norm.normalize("Fluorvätesyra")
    assert norm.normalize("Gasol inkl tub") == norm.normalize("Gasol inkl. tub")
    assert norm.normalize("Rengöring/vaskmedel fast") == norm.normalize("Rengörings-/vaskmedel fast")


def test_acceptance_runner_uses_alias_normalization():
    rows = [TaxRow(section="6.1.2", name="Flourvätesyra")]
    expectations = [AcceptanceExpectation(section="6.1.2", expected_count=1, required_names=["Fluorvätesyra"])]

    result = AcceptanceRunner().run(rows, expectations)

    assert result.passed
