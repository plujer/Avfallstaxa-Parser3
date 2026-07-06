"""Reports for Master Rule Repository."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import RuleRepository


class RuleRepositoryReporter:
    HEADERS = [
        "Rule type",
        "Priority",
        "Source sheet",
        "Row",
        "Section",
        "Tax point",
        "Category",
        "Waste type",
        "Unit type",
        "Factor hint",
        "Volume liter",
        "Tax code",
        "Formula",
        "Tax part",
        "Confidence",
        "Source text",
    ]

    def write_txt(self, repo: RuleRepository, path: str | Path = "output/excel/master_rule_repository_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        types = Counter(rule.rule_type for rule in repo.rules)
        sheets = Counter(rule.source_sheet for rule in repo.rules)

        lines = [
            "Master Rule Repository Report",
            "",
            f"Source workbook: {repo.source_workbook}",
            f"Rules: {repo.rule_count}",
            f"Warnings: {len(repo.warnings)}",
            "",
            "Rule types:",
        ]

        for rule_type, count in sorted(types.items()):
            lines.append(f"- {rule_type}: {count}")

        lines.append("")
        lines.append("Top source sheets:")
        for sheet, count in sheets.most_common(15):
            lines.append(f"- {sheet}: {count}")

        if repo.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in repo.warnings:
                lines.append(f"- {warning}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, repo: RuleRepository, path: str | Path = "output/excel/master_rule_repository.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for rule in repo.rules:
                writer.writerow([
                    rule.rule_type,
                    rule.priority,
                    rule.source_sheet,
                    rule.row_number,
                    rule.section,
                    rule.tax_point,
                    rule.category,
                    rule.waste_type,
                    rule.unit_type,
                    rule.factor_hint,
                    rule.container_volume_liter,
                    rule.tax_code,
                    rule.formula,
                    rule.tax_part,
                    f"{rule.confidence:.2f}",
                    rule.source_text,
                ])

        return out
