"""Write Variant Intelligence reports."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import VariantIntelligenceReport


class VariantIntelligenceReporter:
    def write(self, report: VariantIntelligenceReport, out_dir: str | Path = "output/excel") -> None:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        self.write_text(report, out_path / "variant_intelligence_report.txt")
        self.write_csv(report, out_path / "variant_profiles.csv")

    def write_text(self, report: VariantIntelligenceReport, path: str | Path) -> None:
        family_counts = Counter(profile.family_code for profile in report.profiles if profile.family_code)
        lines = [
            "Variant Intelligence Report",
            "",
            "Status: Tolkar variantdimensioner inom taxefamiljer som beslutsstöd.",
            "Taxa_från_edp ändras inte och kommununik data delas inte.",
            f"Profiles: {report.total_profiles}",
            f"Families: {report.families}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Largest variant families:",
        ]
        for family_code, count in family_counts.most_common(20):
            variants = sorted({profile.variant_key for profile in report.profiles if profile.family_code == family_code})
            lines.append(f"- {family_code}: {count} profil(er), varianter={', '.join(variants[:8])}")
        if report.warnings:
            lines += ["", "Warnings:"] + [f"- {warning}" for warning in report.warnings[:50]]
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_csv(self, report: VariantIntelligenceReport, path: str | Path) -> None:
        with Path(path).open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "tax_code",
                    "family_code",
                    "variant_key",
                    "volume_liter",
                    "waste_code",
                    "interval",
                    "variant",
                    "usage_type",
                    "source",
                    "source_text",
                ],
                delimiter=";",
            )
            writer.writeheader()
            for profile in sorted(report.profiles, key=lambda item: (item.family_code, item.variant_key, item.tax_code)):
                writer.writerow(
                    {
                        "tax_code": profile.tax_code,
                        "family_code": profile.family_code,
                        "variant_key": profile.variant_key,
                        "volume_liter": profile.volume_liter,
                        "waste_code": profile.waste_code,
                        "interval": profile.interval,
                        "variant": profile.variant,
                        "usage_type": profile.usage_type,
                        "source": profile.source,
                        "source_text": profile.source_text,
                    }
                )
