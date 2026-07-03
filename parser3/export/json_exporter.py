"""Export tax rows as JSON."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from parser3.models import TaxRow


class JsonExporter:
    def export(self, rows: list[TaxRow], path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(row) for row in rows]
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return out
