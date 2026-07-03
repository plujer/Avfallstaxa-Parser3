"""Write golden master YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class GoldenMasterWriter:
    def write(self, data: dict[str, Any], path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
        return out
