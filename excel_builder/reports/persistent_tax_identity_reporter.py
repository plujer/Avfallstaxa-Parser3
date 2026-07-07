"""Report writer for persistent tax identities."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models.persistent_tax_identity_models import PersistentTaxIdentityReport


class PersistentTaxIdentityReporter:
    HEADERS = [
        "PersistentTaxID",
        "SectionBoundWordTaxID",
        "ContentFingerprint",
        "IdentityBasis",
        "Occurrence",
        "Status",
        "Word paragraf",
        "Word taxapunkt",
        "Word variant",
        "Word enhet",
        "Kommentar",
    ]

    def write_txt(self, report: PersistentTaxIdentityReport, path: str | Path = "output/excel/persistent_tax_identity_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "Persistent Tax Identity Report",
            "",
            "Syfte:",
            "Skapar permanent intern identitet för varje Word-taxepunkt.",
            "Identiteten är versionsoberoende och ska kunna överleva flytt mellan paragrafer.",
            "",
            "Regler:",
            "- PersistentTaxID är inte en EDP-taxekod.",
            "- Taxa_från_edp är fortsatt facit och ändras aldrig.",
            "- Word-master och Excel-master ändras aldrig.",
            "- Dubbletter av samma innehåll är granskningsinformation, inte automatiskt fel.",
            "",
            f"Total identities: {report.total}",
            f"Duplicate content groups: {report.duplicate_content_groups}",
            f"Warnings: {len(report.warnings)}",
            f"Passed: {report.passed}",
            "",
            "Details:",
        ]
        for item in report.identities:
            lines.append(
                f"- {item.persistent_tax_id} | {item.section_bound_word_tax_id} | "
                f"{item.parser_row.section} | {item.parser_row.tax_point} | occurrence={item.occurrence} | {item.comment}"
            )
        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: PersistentTaxIdentityReport, path: str | Path = "output/excel/persistent_tax_identity.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)
            for item in report.identities:
                writer.writerow([
                    item.persistent_tax_id,
                    item.section_bound_word_tax_id,
                    item.content_fingerprint,
                    item.identity_basis,
                    item.occurrence,
                    item.status,
                    item.parser_row.section,
                    item.parser_row.tax_point,
                    item.parser_row.variant,
                    item.parser_row.unit,
                    item.comment,
                ])
        return out
