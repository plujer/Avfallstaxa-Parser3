"""Write Semantic Attribute Intelligence reports."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import SemanticAttributeReport


class SemanticAttributeReporter:
    def write(self, report: SemanticAttributeReport, out_dir: str | Path = "output/excel") -> None:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        self.write_text(report, out_path / "semantic_attribute_report.txt")
        self.write_csv(report, out_path / "semantic_attributes.csv")

    def write_text(self, report: SemanticAttributeReport, path: str | Path) -> None:
        material_counts = Counter(value for profile in report.profiles for value in profile.materials)
        waste_counts = Counter(value for profile in report.profiles for value in profile.waste_types)
        lines = [
            "Semantic Attribute Intelligence Report",
            "",
            "Status: Extraherar semantiska attribut som beslutsstöd.",
            "Taxa_från_edp ändras inte och kommununik data delas inte.",
            f"Profiles: {report.total_profiles}",
            f"Profiles with attributes: {report.profiles_with_attributes}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Top materials:",
        ]
        for value, count in material_counts.most_common(20):
            lines.append(f"- {value}: {count}")
        lines.append("")
        lines.append("Top waste types:")
        for value, count in waste_counts.most_common(20):
            lines.append(f"- {value}: {count}")
        if report.warnings:
            lines += ["", "Warnings:"] + [f"- {warning}" for warning in report.warnings[:50]]
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_csv(self, report: SemanticAttributeReport, path: str | Path) -> None:
        with Path(path).open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "tax_code",
                    "attribute_key",
                    "attribute_count",
                    "materials",
                    "waste_types",
                    "units",
                    "container_types",
                    "intervals",
                    "property_types",
                    "source",
                    "source_text",
                ],
                delimiter=";",
            )
            writer.writeheader()
            for profile in sorted(report.profiles, key=lambda item: (item.attribute_key, item.tax_code, item.source)):
                writer.writerow(
                    {
                        "tax_code": profile.tax_code,
                        "attribute_key": profile.attribute_key,
                        "attribute_count": profile.attribute_count,
                        "materials": ",".join(profile.materials),
                        "waste_types": ",".join(profile.waste_types),
                        "units": ",".join(profile.units),
                        "container_types": ",".join(profile.container_types),
                        "intervals": ",".join(profile.intervals),
                        "property_types": ",".join(profile.property_types),
                        "source": profile.source,
                        "source_text": profile.source_text,
                    }
                )
