"""Reports for extracted tax knowledge features."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import TaxKnowledgeReport


class KnowledgeReporter:
    HEADERS = [
        "Paragraf",
        "Taxapunkt",
        "Variant",
        "Enhet",
        "Section group",
        "Kategori",
        "Avfallstyp",
        "Enhetstyp",
        "Behållarvolym liter",
        "Faktorhint",
        "Confidence",
        "Keywords",
        "Notes",
    ]

    def write_txt(self, report: TaxKnowledgeReport, path: str | Path = "output/excel/tax_knowledge_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        categories = Counter(item.category for item in report.features)
        factors = Counter(item.factor_hint for item in report.features)

        lines = [
            "Tax Knowledge Report",
            "",
            "Status: Strukturerad kunskap från Word/parsern. Ingen EDP ändras.",
            f"Total: {report.total}",
            "",
            "Kategorier:",
        ]

        for key, count in sorted(categories.items()):
            lines.append(f"- {key or '(tom)'}: {count}")

        lines.append("")
        lines.append("Faktorhint:")
        for key, count in sorted(factors.items()):
            lines.append(f"- {key or '(tom)'}: {count}")

        lines.append("")
        lines.append("Details:")
        for item in report.features:
            lines.append(
                f"- {item.parser_row.section} | {item.parser_row.tax_point} | "
                f"category={item.category} waste={item.waste_type} unit={item.unit_type} "
                f"factor={item.factor_hint} confidence={item.confidence:.2f}"
            )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: TaxKnowledgeReport, path: str | Path = "output/excel/tax_knowledge_features.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for item in report.features:
                writer.writerow([
                    item.parser_row.section,
                    item.parser_row.tax_point,
                    item.parser_row.variant,
                    item.parser_row.unit,
                    item.section_group,
                    item.category,
                    item.waste_type,
                    item.unit_type,
                    item.container_volume_liter,
                    item.factor_hint,
                    f"{item.confidence:.2f}",
                    ", ".join(item.keywords),
                    " | ".join(item.notes),
                ])

        return out
