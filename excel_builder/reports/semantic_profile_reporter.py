"""Reports for semantic tax profiles."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import TaxSemanticProfileReport


class SemanticProfileReporter:
    HEADERS = [
        "Source",
        "Source ID",
        "Tax code",
        "Standard tax code",
        "Category",
        "Waste type",
        "Service type",
        "Container type",
        "Container volume liter",
        "Interval",
        "Property type",
        "Unit type",
        "Factor hint",
        "Confidence",
        "Source text",
    ]

    def write_txt(self, report: TaxSemanticProfileReport, path: str | Path = "output/excel/semantic_profile_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        sources = Counter(profile.source for profile in report.profiles)
        categories = Counter(profile.key.category for profile in report.profiles)
        waste_types = Counter(profile.key.waste_type for profile in report.profiles)

        lines = [
            "Tax Semantic Profile Report",
            "",
            "Status: Gemensam semantisk taxaprofil för Word, standardtaxor och regelrepository.",
            "Profilerna ändrar inte Taxa_från_edp.",
            f"Profiles: {report.total}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Sources:",
        ]

        for key, count in sorted(sources.items()):
            lines.append(f"- {key}: {count}")

        lines.append("")
        lines.append("Categories:")
        for key, count in sorted(categories.items()):
            lines.append(f"- {key or '(tom)'}: {count}")

        lines.append("")
        lines.append("Waste types:")
        for key, count in sorted(waste_types.items()):
            lines.append(f"- {key or '(tom)'}: {count}")

        if report.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in report.warnings:
                lines.append(f"- {warning}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: TaxSemanticProfileReport, path: str | Path = "output/excel/semantic_profiles.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)
            for profile in report.profiles:
                key = profile.key
                writer.writerow([
                    profile.source,
                    profile.source_id,
                    profile.tax_code,
                    profile.standard_tax_code,
                    key.category,
                    key.waste_type,
                    key.service_type,
                    key.container_type,
                    key.container_volume_liter,
                    key.interval,
                    key.property_type,
                    key.unit_type,
                    key.factor_hint,
                    f"{profile.confidence:.2f}",
                    profile.source_text,
                ])

        return out
