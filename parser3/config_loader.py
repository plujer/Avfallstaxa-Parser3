"""Configuration loading for Parser 3.0."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from parser3.utils.exceptions import ConfigurationError


def load_config(path: str | Path = "parser3/config/parser.yaml") -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigurationError(f"Config file not found: {config_path}")

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        raise ConfigurationError(f"Could not read config: {config_path}") from exc

    if not isinstance(data, dict):
        raise ConfigurationError("Config root must be a mapping/object.")

    return data
