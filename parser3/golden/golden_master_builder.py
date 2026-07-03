"""Build golden master from manually verified rows."""

from __future__ import annotations

from collections import defaultdict
from parser3.golden.facit_row import FacitRow


class GoldenMasterBuilder:
    def build(self, rows: list[FacitRow]) -> dict:
        sections: dict[str, dict] = defaultdict(lambda: {"title": "", "tax_count": 0, "rows": []})

        for row in rows:
            section = sections[row.section]
            section["rows"].append(row.to_dict())

        for section in sections.values():
            section["tax_count"] = sum(1 for row in section["rows"] if row.get("export", True))

        return {"sections": dict(sections)}

    def from_tax_rows(self, tax_rows) -> dict:
        rows = [
            FacitRow(
                section=row.section,
                group=row.group,
                name=row.name,
                variant=row.variant,
                unit=row.unit,
                ewc=row.ewc,
                un_number=row.un_number,
                export=row.export,
            )
            for row in tax_rows
        ]
        return self.build(rows)
