"""Validate that every Word/parser tax row exists in Taxepunkter.

Core invariant:
Every tax found in the Word document must be represented as its own row in the
Taxepunkter sheet, regardless of whether Taxa_från_edp is empty or has a match.
"""

from __future__ import annotations

from excel_builder.matching import MatchNormalizer
from excel_builder.models import CoverageItem, CoverageReport, ParserTaxRow, WorkbookTaxRow


class WordTaxCoverageValidator:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def validate(self, parser_rows: list[ParserTaxRow], workbook_rows: list[WorkbookTaxRow]) -> CoverageReport:
        report = CoverageReport()

        exact_index: dict[str, list[WorkbookTaxRow]] = {}
        weak_index: dict[str, list[WorkbookTaxRow]] = {}

        for workbook_row in workbook_rows:
            exact_key = self.normalizer.row_key(
                workbook_row.section,
                workbook_row.tax_point,
                workbook_row.variant,
                workbook_row.unit,
            )
            weak_key = self.normalizer.weak_key(workbook_row.section, workbook_row.tax_point)

            exact_index.setdefault(exact_key, []).append(workbook_row)
            weak_index.setdefault(weak_key, []).append(workbook_row)

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
                report.items.append(
                    CoverageItem(
                        parser_row=parser_row,
                        workbook_row=exact_matches[0],
                        status="COVERED",
                        method="exact row",
                    )
                )
                continue

            if len(exact_matches) > 1:
                report.items.append(
                    CoverageItem(
                        parser_row=parser_row,
                        workbook_row=exact_matches[0],
                        status="REVIEW",
                        method="duplicate exact row",
                        comment=f"{len(exact_matches)} Taxepunkter rows match same parser row",
                    )
                )
                continue

            weak_matches = weak_index.get(weak_key, [])
            if len(weak_matches) == 1:
                report.items.append(
                    CoverageItem(
                        parser_row=parser_row,
                        workbook_row=weak_matches[0],
                        status="COVERED",
                        method="section+tax_point",
                        comment="Variant/enhet skiljer men Word-taxan finns som egen rad",
                    )
                )
                continue

            if len(weak_matches) > 1:
                report.items.append(
                    CoverageItem(
                        parser_row=parser_row,
                        workbook_row=weak_matches[0],
                        status="REVIEW",
                        method="multiple section+tax_point rows",
                        comment=f"{len(weak_matches)} Taxepunkter rows share section+tax_point",
                    )
                )
                continue

            report.items.append(
                CoverageItem(
                    parser_row=parser_row,
                    workbook_row=None,
                    status="MISSING",
                    method="no Taxepunkter row",
                    comment="Word-taxan måste skapas som egen rad i Taxepunkter, oavsett EDP",
                )
            )

        return report
