from parser3.acceptance import AcceptanceExpectation, AcceptanceRunner
from parser3.models import TaxRow


def test_acceptance_runner_passes_count_and_required_names():
    rows = [
        TaxRow(section="6.1.2", name="Asbest, emballerat"),
        TaxRow(section="6.1.2", name="Smittförande avfall"),
    ]
    expectations = [
        AcceptanceExpectation(
            section="6.1.2",
            expected_count=2,
            required_names=["Asbest, emballerat"],
            ignored_names=["Toner, färgpatron utan elektronik"],
        )
    ]

    result = AcceptanceRunner().run(rows, expectations)

    assert result.passed
    assert result.expected_total == 2
    assert result.actual_total == 2


def test_acceptance_runner_fails_wrong_count():
    rows = [TaxRow(section="6.1.2", name="Asbest, emballerat")]
    expectations = [AcceptanceExpectation(section="6.1.2", expected_count=2)]

    result = AcceptanceRunner().run(rows, expectations)

    assert not result.passed


def test_acceptance_runner_fails_ignored_export():
    rows = [TaxRow(section="6.1.2", name="Toner, färgpatron utan elektronik")]
    expectations = [
        AcceptanceExpectation(
            section="6.1.2",
            expected_count=0,
            ignored_names=["Toner, färgpatron utan elektronik"],
        )
    ]

    result = AcceptanceRunner().run(rows, expectations)

    assert not result.passed
    assert result.sections[0].wrongly_exported_ignored
