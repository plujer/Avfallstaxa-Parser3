from parser3.acceptance import AcceptanceRunner, FacitYamlLoader
from parser3.models import TaxRow


def test_acceptance_can_pass_612_yaml_expectation():
    expectations = FacitYamlLoader().load("parser_facit.yaml")
    expectation = [item for item in expectations if item.section == "6.1.2"]
    rows = [TaxRow(section="6.1.2", name=name) for name in expectation[0].required_names]

    result = AcceptanceRunner().run(rows, expectation)

    assert result.passed
    assert result.expected_total == 103
    assert result.actual_total == 103
