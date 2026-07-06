"""Create one consolidated decision per Word/parser tax row.

Priority:
1. Confirmed municipality EDP / Taxepunkter match
2. Standard tax proposal
3. Manual review / new taxa

Existing Taxa_från_edp is always fixed and is never overwritten.
"""

from __future__ import annotations

from excel_builder.matching import MatchNormalizer
from excel_builder.models import (
    ParserTaxRow,
    StandardTaxSuggestionReport,
    TaxDecision,
    TaxDecisionReport,
    WorkbookTaxRow,
)


class TaxDecisionEngine:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def decide(
        self,
        parser_rows: list[ParserTaxRow],
        workbook_rows: list[WorkbookTaxRow],
        standard_suggestions: StandardTaxSuggestionReport | None = None,
    ) -> TaxDecisionReport:
        report = TaxDecisionReport()

        workbook_exact: dict[str, list[WorkbookTaxRow]] = {}
        workbook_weak: dict[str, list[WorkbookTaxRow]] = {}

        for row in workbook_rows:
            exact_key = self.normalizer.row_key(row.section, row.tax_point, row.variant, row.unit)
            weak_key = self.normalizer.weak_key(row.section, row.tax_point)
            workbook_exact.setdefault(exact_key, []).append(row)
            workbook_weak.setdefault(weak_key, []).append(row)

        suggestion_by_key = {}
        if standard_suggestions:
            for suggestion in standard_suggestions.suggestions:
                key = self.normalizer.weak_key(
                    suggestion.parser_row.section,
                    suggestion.parser_row.tax_point,
                )
                suggestion_by_key[key] = suggestion

        for parser_row in parser_rows:
            exact_key = self.normalizer.row_key(
                parser_row.section,
                parser_row.tax_point,
                parser_row.variant,
                parser_row.unit,
            )
            weak_key = self.normalizer.weak_key(parser_row.section, parser_row.tax_point)

            exact_matches = workbook_exact.get(exact_key, [])
            if len(exact_matches) == 1:
                wb = exact_matches[0]
                if wb.tax_code:
                    report.decisions.append(
                        TaxDecision(
                            parser_row=parser_row,
                            workbook_row=wb,
                            status="EDP_MATCH",
                            source="Taxepunkter/Taxa_från_edp",
                            rule="Befintlig Taxakod i Taxepunkter behålls",
                            confidence=1.0,
                            comment="Bekräftad kommun-EDP har högsta prioritet.",
                        )
                    )
                else:
                    report.decisions.append(
                        TaxDecision(
                            parser_row=parser_row,
                            workbook_row=wb,
                            status="REVIEW_REQUIRED",
                            source="Taxepunkter",
                            rule="Word-taxan finns som rad men saknar Taxakod",
                            confidence=0.80,
                            comment="Rad finns. EDP-koppling behöver granskas eller kompletteras.",
                        )
                    )
                continue

            if len(exact_matches) > 1:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        workbook_row=exact_matches[0],
                        status="REVIEW_REQUIRED",
                        source="Taxepunkter",
                        rule="Dubblett i befintliga Taxepunkter",
                        confidence=0.50,
                        comment=f"{len(exact_matches)} rader matchar exakt. Manuell granskning krävs.",
                    )
                )
                continue

            weak_matches = workbook_weak.get(weak_key, [])
            if len(weak_matches) == 1:
                wb = weak_matches[0]
                if wb.tax_code:
                    report.decisions.append(
                        TaxDecision(
                            parser_row=parser_row,
                            workbook_row=wb,
                            status="EDP_MATCH",
                            source="Taxepunkter/Taxa_från_edp",
                            rule="Befintlig Taxakod i Taxepunkter behålls via paragraf+taxapunkt",
                            confidence=0.90,
                            comment="Variant/enhet skiljer eller saknas men kommun-EDP behålls.",
                        )
                    )
                else:
                    report.decisions.append(
                        TaxDecision(
                            parser_row=parser_row,
                            workbook_row=wb,
                            status="REVIEW_REQUIRED",
                            source="Taxepunkter",
                            rule="Rad finns men saknar Taxakod",
                            confidence=0.75,
                            comment="Taxa finns som rad. EDP-koppling saknas.",
                        )
                    )
                continue

            suggestion = suggestion_by_key.get(weak_key)
            if suggestion and suggestion.status in {"PROPOSAL", "REVIEW"} and suggestion.standard_row:
                report.decisions.append(
                    TaxDecision(
                        parser_row=parser_row,
                        standard_row=suggestion.standard_row,
                        status="STANDARD_PROPOSAL" if suggestion.status == "PROPOSAL" else "REVIEW_REQUIRED",
                        source="Standardtaxor",
                        rule="Standardtaxa används endast som förslag",
                        confidence=suggestion.score,
                        comment="Standardtaxa får inte skriva över befintlig kommun-EDP.",
                    )
                )
                continue

            report.decisions.append(
                TaxDecision(
                    parser_row=parser_row,
                    status="NEW_TAXA",
                    source="Word",
                    rule="Word-taxa saknar EDP-match och standardförslag",
                    confidence=0.0,
                    comment="Skapa/hantera som ny taxa eller manuell granskning.",
                )
            )

        return report
