"""Load golden master YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class GoldenMasterLoader:
    def load(self, path: str | Path) -> dict[str, Any]:
        p = Path(path)
        if not p.exists():
            return {"sections": {}}
        with p.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            return {"sections": {}}
        return data
