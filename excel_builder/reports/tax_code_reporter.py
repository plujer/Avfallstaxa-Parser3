"""Reports for parsed tax codes."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import TaxCodeParseReport


class TaxCodeReporter:
    HEADERS = [
        "Tax code",
        "Prefix",
        "Container type",
        "Volume liter",
        "Waste code",
        "Waste type",
        "Interval",
        "Variant",
        "Suffix",
        "Family key",
        "Confidence",
        "Notes",
    ]

    def write_txt(self, report: TaxCodeParseReport, path: str | Path = "output/excel/tax_code_intelligence_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        prefixes = Counter(item.prefix for item in report.parsed_codes)
        families = Counter(item.family_key for item in report.parsed_codes if item.family_key)

        lines = [
            "Tax Code Intelligence Report",
            "",
            "Status: Taxekoder delas upp i semantiska delar. Inga EDP-data ändras.",
            f"Tax codes: {report.total}",
            f"With family key: {report.parsed_with_family}",
            "",
            "Prefixes:",
        ]

        for prefix, count in sorted(prefixes.items()):
            lines.append(f"- {prefix or '(okänd)'}: {count}")

        lines.append("")
        lines.append("Top families:")
        for family, count in families.most_common(30):
            lines.append(f"- {family}: {count}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: TaxCodeParseReport, path: str | Path = "output/excel/tax_code_intelligence.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)
            for item in report.parsed_codes:
                writer.writerow([
                    item.original_code,
                    item.prefix,
                    item.container_type,
                    item.volume_liter,
                    item.waste_code,
                    item.waste_type,
                    item.interval,
                    item.variant,
                    item.suffix,
                    item.family_key,
                    f"{item.confidence:.2f}",
                    " | ".join(item.notes),
                ])

        return out
