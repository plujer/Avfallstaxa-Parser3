"""Read Parser3 result JSON as matching rows."""

from __future__ import annotations

import json
from pathlib import Path

from excel_builder.models import ParserTaxRow


class ParserMatchReader:
    def read(self, path: str | Path = "output/reports/parser3_result.json") -> list[ParserTaxRow]:
        source = Path(path)
        if not source.exists():
            return []

        data = json.loads(source.read_text(encoding="utf-8"))
        rows: list[ParserTaxRow] = []

        for item in data:
            if not isinstance(item, dict):
                continue
            if item.get("export") is False:
                continue

            rows.append(
                ParserTaxRow(
                    section=str(item.get("section", "") or ""),
                    tax_point=str(item.get("name", "") or ""),
                    variant=str(item.get("variant", "") or ""),
                    unit=str(item.get("unit", "") or ""),
                    price=str(item.get("price", "") or ""),
                )
            )

        return rows
