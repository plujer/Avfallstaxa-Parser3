"""Create a simple text report."""

from __future__ import annotations

from pathlib import Path

from parser3.models import TaxRow


class TextReporter:
    def write(self, rows: list[TaxRow], path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "Avfallstaxa Parser 3.0 report",
            f"Tax rows: {len(rows)}",
            "",
        ]
        for row in rows:
            lines.append(f"{row.section} | {row.group} | {row.name} | {row.variant} | {row.unit} | {row.price}")
        out.write_text("\\n".join(lines), encoding="utf-8")
        return out
