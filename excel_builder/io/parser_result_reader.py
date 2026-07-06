"""Read Parser3 output JSON into Excel Builder rows."""

from __future__ import annotations

import json
from pathlib import Path

from excel_builder.models import BuilderInputRow, BuilderResult


class ParserResultReader:
    def read(self, path: str | Path = "output/reports/parser3_result.json") -> BuilderResult:
        source = Path(path)
        result = BuilderResult()

        if not source.exists():
            result.warnings.append(f"Parser result saknas: {source}")
            return result

        data = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            result.warnings.append("Parser result är inte en lista.")
            return result

        for item in data:
            if not isinstance(item, dict):
                continue
            if item.get("export") is False:
                continue

            result.rows.append(
                BuilderInputRow(
                    section=str(item.get("section", "") or ""),
                    name=str(item.get("name", "") or ""),
                    variant=str(item.get("variant", "") or ""),
                    unit=str(item.get("unit", "") or ""),
                    price=str(item.get("price", "") or ""),
                    group=str(item.get("group", "") or ""),
                    source="parser3_result.json",
                )
            )

        return result
