"""Write Tax Family Intelligence reports."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import TaxFamilyReport


class TaxFamilyReporter:
    def write(self, report: TaxFamilyReport, out_dir: str | Path = "output/excel") -> None:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        self.write_text(report, out_path / "tax_family_report.txt")
        self.write_csv(report, out_path / "tax_families.csv")

    def write_text(self, report: TaxFamilyReport, path: str | Path) -> None:
        lines = [
            "Tax Family Intelligence Report",
            "",
            "Status: Grupperar taxekoder i familjer som beslutsstöd.",
            "Taxa_från_edp ändras inte och kommununik data delas inte.",
            f"Families: {report.total_families}",
            f"Members: {report.total_members}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Largest families:",
        ]
        for family in sorted(report.families, key=lambda item: item.member_count, reverse=True)[:20]:
            lines.append(
                f"- {family.family_code}: {family.member_count} kod(er), "
                f"intervall={','.join(family.intervals) or '-'}, "
                f"varianter={','.join(family.variants) or '-'}"
            )
        if report.warnings:
            lines += ["", "Warnings:"] + [f"- {warning}" for warning in report.warnings[:50]]
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_csv(self, report: TaxFamilyReport, path: str | Path) -> None:
        with Path(path).open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "family_code",
                    "tax_code",
                    "prefix",
                    "volume_liter",
                    "waste_code",
                    "interval",
                    "variant",
                    "source",
                    "confidence",
                    "notes",
                ],
                delimiter=";",
            )
            writer.writeheader()
            for family in sorted(report.families, key=lambda item: item.family_code):
                for member in family.members:
                    parsed = member.parsed
                    writer.writerow(
                        {
                            "family_code": family.family_code,
                            "tax_code": member.tax_code,
                            "prefix": member.family_key.prefix,
                            "volume_liter": member.family_key.volume_liter,
                            "waste_code": member.family_key.waste_code,
                            "interval": member.interval,
                            "variant": member.variant,
                            "source": member.source,
                            "confidence": parsed.confidence if parsed else "",
                            "notes": " | ".join(parsed.notes) if parsed else "",
                        }
                    )
