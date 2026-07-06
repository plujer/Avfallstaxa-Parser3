"""Build a complete row plan for Taxepunkter from Word/parser rows.

Core rule:
Every tax found in the Word document must exist as its own row in Taxepunkter.
Taxa_från_edp may enrich rows, but it must never decide if a Word tax exists.
"""

from __future__ import annotations

from excel_builder.matching import MatchNormalizer
from excel_builder.models import ParserTaxRow, TaxepunkterBuildPlan, TaxepunkterBuildRow, WorkbookTaxRow


class TaxepunkterRowBuilder:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def build_plan(self, parser_rows: list[ParserTaxRow], workbook_rows: list[WorkbookTaxRow]) -> TaxepunkterBuildPlan:
        plan = TaxepunkterBuildPlan()

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
                plan.rows.append(
                    TaxepunkterBuildRow(
                        parser_row=parser_row,
                        workbook_row=exact_matches[0],
                        action="REUSE",
                        method="exact Taxepunkter row",
                        comment="Word-taxan finns redan som egen rad",
                    )
                )
                continue

            if len(exact_matches) > 1:
                plan.rows.append(
                    TaxepunkterBuildRow(
                        parser_row=parser_row,
                        workbook_row=exact_matches[0],
                        action="REVIEW",
                        method="duplicate exact Taxepunkter rows",
                        comment=f"{len(exact_matches)} befintliga rader matchar exakt",
                    )
                )
                continue

            weak_matches = weak_index.get(weak_key, [])
            if len(weak_matches) == 1:
                plan.rows.append(
                    TaxepunkterBuildRow(
                        parser_row=parser_row,
                        workbook_row=weak_matches[0],
                        action="REUSE",
                        method="section+tax_point",
                        comment="Word-taxan finns som egen rad; variant/enhet kan kompletteras från Word",
                    )
                )
                continue

            if len(weak_matches) > 1:
                plan.rows.append(
                    TaxepunkterBuildRow(
                        parser_row=parser_row,
                        workbook_row=weak_matches[0],
                        action="REVIEW",
                        method="multiple section+tax_point rows",
                        comment=f"{len(weak_matches)} befintliga rader delar paragraf+taxapunkt",
                    )
                )
                continue

            plan.rows.append(
                TaxepunkterBuildRow(
                    parser_row=parser_row,
                    workbook_row=None,
                    action="CREATE",
                    method="word tax missing from Taxepunkter",
                    comment="Skapa egen rad i Taxepunkter oavsett EDP-status",
                )
            )

        return plan
