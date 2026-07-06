"""First matching engine for Parser rows -> current Arbets-Excel rows.

This block is read-only. It does not write to the reference workbook.
"""

from __future__ import annotations

from difflib import SequenceMatcher

from excel_builder.matching.match_normalizer import MatchNormalizer
from excel_builder.models import MatchCandidate, MatchReport, ParserTaxRow, WorkbookTaxRow


class MatchingEngine:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def match(self, parser_rows: list[ParserTaxRow], workbook_rows: list[WorkbookTaxRow]) -> MatchReport:
        report = MatchReport()

        exact_index: dict[str, list[WorkbookTaxRow]] = {}
        weak_index: dict[str, list[WorkbookTaxRow]] = {}

        for row in workbook_rows:
            exact_key = self.normalizer.row_key(row.section, row.tax_point, row.variant, row.unit)
            weak_key = self.normalizer.weak_key(row.section, row.tax_point)
            exact_index.setdefault(exact_key, []).append(row)
            weak_index.setdefault(weak_key, []).append(row)

        for parser_row in parser_rows:
            exact_key = self.normalizer.row_key(
                parser_row.section,
                parser_row.tax_point,
                parser_row.variant,
                parser_row.unit,
            )
            weak_key = self.normalizer.weak_key(parser_row.section, parser_row.tax_point)

            exact_matches = exact_index.get(exact_key, [])
            if len(exact_matches) == 1:
                report.candidates.append(
                    MatchCandidate(
                        parser_row=parser_row,
                        workbook_row=exact_matches[0],
                        status="EXACT",
                        method="section+tax_point+variant+unit",
                        score=1.0,
                    )
                )
                continue

            if len(exact_matches) > 1:
                report.candidates.append(
                    MatchCandidate(
                        parser_row=parser_row,
                        workbook_row=exact_matches[0],
                        status="REVIEW",
                        method="duplicate exact key",
                        score=1.0,
                        comment=f"{len(exact_matches)} exact workbook rows found",
                    )
                )
                continue

            weak_matches = weak_index.get(weak_key, [])
            if len(weak_matches) == 1:
                report.candidates.append(
                    MatchCandidate(
                        parser_row=parser_row,
                        workbook_row=weak_matches[0],
                        status="PROBABLE",
                        method="section+tax_point",
                        score=0.90,
                        comment="Variant/enhet skiljer eller saknas",
                    )
                )
                continue

            fuzzy = self._best_fuzzy(parser_row, workbook_rows)
            if fuzzy and fuzzy[1] >= 0.86:
                report.candidates.append(
                    MatchCandidate(
                        parser_row=parser_row,
                        workbook_row=fuzzy[0],
                        status="REVIEW",
                        method="fuzzy same section",
                        score=fuzzy[1],
                        comment="Behöver manuell kontroll innan EDP-kod återanvänds",
                    )
                )
                continue

            report.candidates.append(
                MatchCandidate(
                    parser_row=parser_row,
                    workbook_row=None,
                    status="NEW",
                    method="no match",
                    score=0.0,
                    comment="Ny rad behövs i Arbets-Excel",
                )
            )

        return report

    def _best_fuzzy(self, parser_row: ParserTaxRow, workbook_rows: list[WorkbookTaxRow]) -> tuple[WorkbookTaxRow, float] | None:
        parser_section = self.normalizer.normalize(parser_row.section)
        parser_name = self.normalizer.normalize(parser_row.tax_point)

        best_row: WorkbookTaxRow | None = None
        best_score = 0.0

        for row in workbook_rows:
            if self.normalizer.normalize(row.section) != parser_section:
                continue
            score = SequenceMatcher(None, parser_name, self.normalizer.normalize(row.tax_point)).ratio()
            if score > best_score:
                best_score = score
                best_row = row

        if best_row is None:
            return None
        return best_row, best_score
