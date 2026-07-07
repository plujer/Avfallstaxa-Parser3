"""Semantic Decision Engine.

Integrates Semantic Candidate Ranking into the final tax decisions.

Principles:
- Existing municipality EDP / Taxa_från_edp remains highest priority.
- Standard taxes are suggestions only.
- Candidates without tax code are review support, not automatic code decisions.
- If top candidates are too close, require manual review.
"""

from __future__ import annotations

from collections import defaultdict

from excel_builder.models import (
    ParserTaxRow,
    SemanticCandidate,
    TaxDecision,
    TaxDecisionReport,
)


class SemanticDecisionEngine:
    AUTO_MATCH_THRESHOLD = 0.98
    STANDARD_PROPOSAL_THRESHOLD = 0.88
    REVIEW_THRESHOLD = 0.72
    AMBIGUITY_DELTA = 0.03

    SOURCE_PRIORITY_BONUS = {
        "RULE:EDP": 0.10,
        "RULE:TAXEPUNKT": 0.05,
        "STANDARD": 0.00,
    }

    SOURCE_PRIORITY_LABEL = {
        "RULE:EDP": "Kommunens EDP",
        "RULE:TAXEPUNKT": "Taxepunkter",
        "STANDARD": "Standardtaxor",
    }

    def decide(
        self,
        parser_rows: list[ParserTaxRow],
        semantic_candidates: list[SemanticCandidate],
    ) -> TaxDecisionReport:
        report = TaxDecisionReport()
        candidates_by_word = defaultdict(list)

        for candidate in semantic_candidates:
            candidates_by_word[candidate.word_profile.source_id].append(candidate)

        for idx, parser_row in enumerate(parser_rows, start=1):
            source_id = f"WORD:{idx}"
            ranked = self._rank_with_source_priority(candidates_by_word.get(source_id, []))

            if not ranked:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        status="NEW_TAXA",
                        source="SemanticDecisionEngine",
                        rule="Ingen semantisk kandidat hittades",
                        confidence=0.0,
                        comment="Skapa/hantera som ny taxa eller komplettera regelverk.",
                    )
                )
                continue

            best = ranked[0]
            second = ranked[1] if len(ranked) > 1 else None
            adjusted_score = self._adjusted_score(best)
            ambiguous = self._is_ambiguous(best, second)

            candidate_profile = best.candidate_profile
            has_tax_code = bool(candidate_profile.tax_code or candidate_profile.standard_tax_code)

            if ambiguous:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        status="REVIEW_REQUIRED",
                        source=self._source_label(candidate_profile.source),
                        rule="Semantiska toppkandidater ligger för nära varandra",
                        confidence=adjusted_score,
                        comment=self._comment(best, prefix="Manuell granskning krävs på grund av liten skillnad mellan kandidater."),
                    )
                )
                continue

            if not has_tax_code:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        status="REVIEW_REQUIRED",
                        source=self._source_label(candidate_profile.source),
                        rule="Bästa semantiska kandidat saknar taxekod",
                        confidence=adjusted_score,
                        comment=self._comment(best, prefix="Kandidaten kan ge beslutsstöd men saknar taxekod."),
                    )
                )
                continue

            if candidate_profile.source == "RULE:EDP" and adjusted_score >= self.AUTO_MATCH_THRESHOLD:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        status="EDP_MATCH",
                        source="Kommunens EDP",
                        rule="Hög semantisk träff mot befintlig kommun-EDP",
                        confidence=adjusted_score,
                        comment=self._comment(best, prefix="Befintlig kommun-EDP har högsta prioritet."),
                    )
                )
                continue

            if candidate_profile.source == "RULE:TAXEPUNKT" and adjusted_score >= self.STANDARD_PROPOSAL_THRESHOLD:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        status="REVIEW_REQUIRED",
                        source="Taxepunkter",
                        rule="Hög semantisk träff mot befintlig Taxepunkter-rad",
                        confidence=adjusted_score,
                        comment=self._comment(best, prefix="Granska innan taxekod används."),
                    )
                )
                continue

            if candidate_profile.source == "STANDARD" and adjusted_score >= self.STANDARD_PROPOSAL_THRESHOLD:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        status="STANDARD_PROPOSAL",
                        source="Standardtaxor",
                        rule="Hög semantisk träff mot standardtaxa",
                        confidence=adjusted_score,
                        standard_row=None,
                        comment=self._comment(best, prefix="Standardtaxa är endast förslag och får inte skriva över kommun-EDP."),
                    )
                )
                continue

            if adjusted_score >= self.REVIEW_THRESHOLD:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        status="REVIEW_REQUIRED",
                        source=self._source_label(candidate_profile.source),
                        rule="Semantisk kandidat finns men säkerheten räcker inte för förslag",
                        confidence=adjusted_score,
                        comment=self._comment(best, prefix="Granska kandidat manuellt."),
                    )
                )
                continue

            report.decisions.append(
                TaxDecision(
                    parser_row=parser_row,
                    status="NEW_TAXA",
                    source="SemanticDecisionEngine",
                    rule="Ingen kandidat över granskningsgräns",
                    confidence=adjusted_score,
                    comment=self._comment(best, prefix="Bästa kandidat var för svag."),
                )
            )

        return report

    def _rank_with_source_priority(self, candidates: list[SemanticCandidate]) -> list[SemanticCandidate]:
        return sorted(
            candidates,
            key=lambda candidate: self._adjusted_score(candidate),
            reverse=True,
        )

    def _adjusted_score(self, candidate: SemanticCandidate) -> float:
        return round(min(candidate.score + self.SOURCE_PRIORITY_BONUS.get(candidate.candidate_profile.source, 0.0), 1.0), 4)

    def _is_ambiguous(self, best: SemanticCandidate, second: SemanticCandidate | None) -> bool:
        if second is None:
            return False

        best_score = self._adjusted_score(best)
        second_score = self._adjusted_score(second)

        if best_score < self.STANDARD_PROPOSAL_THRESHOLD:
            return False

        return abs(best_score - second_score) < self.AMBIGUITY_DELTA

    def _source_label(self, source: str) -> str:
        return self.SOURCE_PRIORITY_LABEL.get(source, source)

    def _comment(self, candidate: SemanticCandidate, prefix: str = "") -> str:
        code = candidate.candidate_profile.tax_code or candidate.candidate_profile.standard_tax_code
        adjusted = self._adjusted_score(candidate)
        base = (
            f"{prefix} Kandidat={candidate.candidate_profile.source} "
            f"{code} score={candidate.score:.2f} justerad={adjusted:.2f}. "
            f"{candidate.explanation}"
        )
        return base.strip()
