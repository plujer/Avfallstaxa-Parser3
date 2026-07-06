"""Reports for the Knowledge Index."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import KnowledgeIndex


class KnowledgeIndexReporter:
    HEADERS = [
        "Kategori",
        "Avfallstyp",
        "Enhetstyp",
        "Faktorhint",
        "Behållarvolym liter",
        "Word feature count",
        "Standard row count",
        "Exempel Word-taxor",
        "Exempel standardtaxor",
    ]

    def write_txt(self, index: KnowledgeIndex, path: str | Path = "output/excel/knowledge_index_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Knowledge Index Report",
            "",
            "Status: Grupperar Word-taxor och standardtaxor inför regelbaserad matchning.",
            "Detta ändrar inte Taxa_från_edp.",
            "",
            f"Index entries: {index.entry_count}",
            f"Standard rows indexed: {index.standard_row_count}",
            f"Warnings: {len(index.warnings)}",
            "",
            "Entries:",
        ]

        for key, entry in sorted(index.entries.items(), key=lambda pair: str(pair[0])):
            lines.append(
                f"- category={key.category or ''} waste={key.waste_type or ''} unit={key.unit_type or ''} "
                f"factor={key.factor_hint or ''} volume={key.container_volume_liter or ''} "
                f"features={entry.feature_count} standards={len(entry.standard_rows)}"
            )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, index: KnowledgeIndex, path: str | Path = "output/excel/knowledge_index.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for key, entry in sorted(index.entries.items(), key=lambda pair: str(pair[0])):
                word_examples = [
                    f"{feature.parser_row.section} {feature.parser_row.tax_point}"
                    for feature in entry.feature_examples
                ]
                standard_examples = [
                    f"{row.strTaxekod} {row.strTaxebenamning}"
                    for row in entry.standard_rows[:5]
                ]

                writer.writerow([
                    key.category,
                    key.waste_type,
                    key.unit_type,
                    key.factor_hint,
                    key.container_volume_liter,
                    entry.feature_count,
                    len(entry.standard_rows),
                    " | ".join(word_examples),
                    " | ".join(standard_examples),
                ])

        return out
