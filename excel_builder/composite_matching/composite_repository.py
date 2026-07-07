"""Build sample composite matching inputs from global reference sources."""

from __future__ import annotations

from excel_builder.models import CompositeMatchInput, CompositeMatchingReport, RuleRepository, StandardTaxCatalog
from excel_builder.composite_matching.composite_matcher import CompositeMatcher


class CompositeMatchingRepository:
    """Creates an explainable composite report from global reference knowledge.

    The repository intentionally uses the standard catalog and master rule
    repository as global knowledge. It does not read or merge municipality-
    specific EDP exports.
    """

    def __init__(self) -> None:
        self.matcher = CompositeMatcher()

    def from_standard_and_rules(self, catalog: StandardTaxCatalog, repository: RuleRepository, limit: int = 500) -> CompositeMatchingReport:
        report = CompositeMatchingReport()
        inputs: list[CompositeMatchInput] = []

        standard_by_code = {
            self._norm(row.strTaxekod): row
            for row in catalog.rows
            if self._norm(row.strTaxekod)
        }

        for rule in repository.rules:
            candidate_code = self._norm(rule.tax_code or rule.standard_tax_code)
            if not candidate_code or candidate_code not in standard_by_code:
                continue
            candidate = standard_by_code[candidate_code]
            word_text = rule.source_text or rule.tax_point or rule.category or rule.waste_type or candidate.strTaxebenamning
            inputs.append(
                CompositeMatchInput(
                    word_tax_code=candidate_code,
                    candidate_tax_code=candidate.strTaxekod,
                    word_text=word_text,
                    candidate_text=candidate.strTaxebenamning,
                    edp_exact_match=bool(rule.tax_code and self._norm(rule.tax_code) == self._norm(candidate.strTaxekod)),
                    standard_proposal=bool(rule.standard_tax_code),
                    same_context=bool(rule.section or rule.category or rule.waste_type),
                    same_structure=bool(rule.section),
                    source=f"{rule.source_sheet}:{rule.row_number}",
                )
            )
            if len(inputs) >= limit:
                break

        if not inputs:
            report.warnings.append("Inga jämförbara standard-/regelrader hittades för composite matching.")
            for row in catalog.rows[: min(limit, 50)]:
                if not self._norm(row.strTaxekod):
                    continue
                inputs.append(
                    CompositeMatchInput(
                        word_tax_code=row.strTaxekod,
                        candidate_tax_code=row.strTaxekod,
                        word_text=row.strTaxebenamning,
                        candidate_text=row.strTaxebenamning,
                        edp_exact_match=True,
                        standard_proposal=False,
                        same_context=False,
                        same_structure=False,
                        source=f"{row.source_sheet}:{row.row_number}",
                    )
                )

        report.results = [self.matcher.compare(item) for item in inputs]
        return report

    def _norm(self, value: str) -> str:
        return str(value or "").strip().upper().replace(" ", "").replace("-", "")
