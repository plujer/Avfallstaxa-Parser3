"""Reports for consolidated tax decisions."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import TaxDecisionReport


class DecisionReporter:
    HEADERS = [
        "Status",
        "Source",
        "Rule",
        "Confidence",
        "Paragraf",
        "Taxapunkt",
        "Variant",
        "Enhet",
        "Excel rad",
        "EDP taxakod",
        "Standard taxakod",
        "Kommentar",
    ]

    def write_txt(self, report: TaxDecisionReport, path: str | Path = "output/excel/tax_decision_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Tax Decision Report",
            "",
            "Priority:",
            "1. Bekräftad kommun-EDP / Taxa_från_edp",
            "2. Word-taxa",
            "3. Standardtaxor endast som förslag",
            "4. Manuell granskning",
            "",
            f"Total: {report.total}",
            f"EDP_MATCH: {report.edp_match}",
            f"STANDARD_PROPOSAL: {report.standard_proposal}",
            f"REVIEW_REQUIRED: {report.review_required}",
            f"NEW_TAXA: {report.new_taxa}",
            "",
            "Details:",
        ]

        for decision in report.decisions:
            wb = decision.workbook_row
            st = decision.standard_row
            lines.append(
                f"- {decision.status} | {decision.parser_row.section} | {decision.parser_row.tax_point} | "
                f"source={decision.source} rule={decision.rule} "
                f"edp={wb.tax_code if wb else ''} standard={st.strTaxekod if st else ''} | {decision.comment}"
            )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: TaxDecisionReport, path: str | Path = "output/excel/tax_decision_results.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for decision in report.decisions:
                wb = decision.workbook_row
                st = decision.standard_row
                writer.writerow([
                    decision.status,
                    decision.source,
                    decision.rule,
                    f"{decision.confidence:.3f}",
                    decision.parser_row.section,
                    decision.parser_row.tax_point,
                    decision.parser_row.variant,
                    decision.parser_row.unit,
                    wb.row_number if wb else "",
                    wb.tax_code if wb else "",
                    st.strTaxekod if st else "",
                    decision.comment,
                ])

        return out
