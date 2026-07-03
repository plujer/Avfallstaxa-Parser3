"""Merge new facit rows into an existing golden master."""

from __future__ import annotations

from parser3.golden.facit_row import FacitRow


class GoldenMasterMerger:
    def merge_rows(self, existing: dict, rows: list[FacitRow]) -> dict:
        data = dict(existing or {})
        sections = dict(data.get("sections", {}) or {})

        for row in rows:
            section = sections.setdefault(
                row.section,
                {"title": "", "tax_count": 0, "rows": []},
            )
            section_rows = section.setdefault("rows", [])

            key = (row.name, row.variant, row.unit, row.group)
            existing_keys = {
                (
                    r.get("name", ""),
                    r.get("variant", ""),
                    r.get("unit", ""),
                    r.get("group", ""),
                )
                for r in section_rows
                if isinstance(r, dict)
            }

            if key not in existing_keys:
                section_rows.append(row.to_dict())

            section["tax_count"] = sum(1 for r in section_rows if r.get("export", True))

        data["sections"] = sections
        return data
