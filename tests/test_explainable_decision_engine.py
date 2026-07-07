from excel_builder.composite_matching import CompositeMatcher
from excel_builder.decision_explainer import ConfidenceCalculator, DecisionTraceBuilder, ExplainableDecisionEngine
from excel_builder.models import CompositeMatchInput, CompositeMatchingReport


def test_confidence_calculator_rewards_edp_and_multiple_strong_signals():
    result = CompositeMatcher().compare(
        CompositeMatchInput(
            word_tax_code="KÄ240RM26",
            candidate_tax_code="KÄ240RM26",
            word_text="240 liter restavfall hämtning 26 gånger per år",
            candidate_text="240 liter restavfall hämtning 26 gånger per år",
            edp_exact_match=True,
            same_context=True,
            same_structure=True,
        )
    )

    confidence = ConfidenceCalculator().calculate(result)

    assert result.status == "MATCH"
    assert confidence >= result.score
    assert confidence <= 1.0


def test_decision_trace_builder_creates_explainable_accept_trace():
    result = CompositeMatcher().compare(
        CompositeMatchInput(
            word_tax_code="KÄ240RM26",
            candidate_tax_code="KÄ240RM26",
            word_text="Kärl 240 liter restavfall 26 hämtningar",
            candidate_text="Kärl 240 liter restavfall 26 hämtningar",
            edp_exact_match=True,
            same_context=True,
            same_structure=True,
        )
    )

    trace = DecisionTraceBuilder().build(result)

    assert trace.decision == "ACCEPT"
    assert trace.confidence >= 0.70
    assert trace.parts
    assert "edp_exact" in trace.primary_reason


def test_explainable_decision_engine_preserves_warnings_and_creates_review_trace():
    result = CompositeMatcher().compare(
        CompositeMatchInput(
            word_tax_code="KÄ240RM26",
            candidate_tax_code="KÄ240RM52",
            word_text="Kärl 240 liter restavfall 26 hämtningar",
            candidate_text="Kärl 240 liter restavfall 52 hämtningar",
            edp_exact_match=False,
            standard_proposal=True,
            same_context=True,
            same_structure=True,
        )
    )
    composite_report = CompositeMatchingReport(results=[result], warnings=["testvarning"])

    report = ExplainableDecisionEngine().explain(composite_report)

    assert report.total_traces == 1
    assert report.review_count + report.accepted_count + report.rejected_count == 1
    assert report.warnings == ["testvarning"]
