"""Reports for the Taxepunkter row build plan."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import TaxepunkterBuildPlan


class RowBuilderReporter:
    HEADERS = [
        "Action",
        "Method",
        "Parser paragraf",
        "Parser taxapunkt",
        "Parser variant",
        "Parser enhet",
        "Excel rad",
        "Excel taxapunkt",
        "Excel variant",
        "Excel enhet",
        "Excel taxakod",
        "Kommentar",
    ]

    def write_txt(self, plan: TaxepunkterBuildPlan, path: str | Path = "output/excel/taxepunkter_row_plan_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Taxepunkter Row Build Plan",
            "",
            "KRAV:",
            "Alla taxor som hittas i Word/parsern ska finnas som egen rad i Taxepunkter.",
            "EDP-data kompletterar endast raden efteråt.",
            "",
            f"Parser rows: {plan.total_parser_rows}",
            f"REUSE: {plan.reuse_count}",
            f"CREATE: {plan.create_count}",
            f"REVIEW: {plan.review_count}",
            f"Coverage plan valid: {plan.passed_coverage}",
            "",
            "Details:",
        ]

        for item in plan.rows:
            wb = item.workbook_row
            lines.append(
                f"- {item.action} | {item.method} | "
                f"{item.parser_row.section} | {item.parser_row.tax_point} | "
                f"excel_row={wb.row_number if wb else ''} tax_code={wb.tax_code if wb else ''} | "
                f"{item.comment}"
            )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, plan: TaxepunkterBuildPlan, path: str | Path = "output/excel/taxepunkter_row_plan.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for item in plan.rows:
                wb = item.workbook_row
                writer.writerow([
                    item.action,
                    item.method,
                    item.parser_row.section,
                    item.parser_row.tax_point,
                    item.parser_row.variant,
                    item.parser_row.unit,
                    wb.row_number if wb else "",
                    wb.tax_point if wb else "",
                    wb.variant if wb else "",
                    wb.unit if wb else "",
                    wb.tax_code if wb else "",
                    item.comment,
                ])

        return out
