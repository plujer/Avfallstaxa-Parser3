"""Explainable Decision Engine.

Turns composite matching results into decision traces that can be reported and
later written back to ArbetsExcel as transparent decision support.
"""

from __future__ import annotations

from excel_builder.decision_explainer.decision_trace import DecisionTraceBuilder
from excel_builder.models import CompositeMatchingReport, ExplainableDecisionReport


class ExplainableDecisionEngine:
    def __init__(self) -> None:
        self.trace_builder = DecisionTraceBuilder()

    def explain(self, composite_report: CompositeMatchingReport) -> ExplainableDecisionReport:
        report = ExplainableDecisionReport()
        report.traces = [self.trace_builder.build(result) for result in composite_report.results]
        report.warnings.extend(composite_report.warnings)
        if not report.traces:
            report.warnings.append("Inga composite matching-resultat fanns att förklara.")
        return report
