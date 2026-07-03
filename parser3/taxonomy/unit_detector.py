"""Unit detection for tax rows."""

from __future__ import annotations

import re


class UnitDetector:
    UNIT_ALIASES = {
        "kilogram": "kilogram",
        "kg": "kilogram",
        "styck": "styck",
        "st": "styck",
        "liter": "liter",
        "m3": "m³",
        "m³": "m³",
        "besök": "besök",
        "tillfälle": "tillfälle",
        "fraktion": "fraktion",
        "container": "container",
        "dygn": "dygn",
        "år": "år",
        "tömning": "tömning",
        "faktura": "faktura",
        "kärl": "kärl",
        "bunt": "bunt",
        "lägenhet": "lägenhet",
        "lyft": "lyft",
    }

    def detect(self, cells: list[str], text: str = "") -> str:
        joined = " ".join(cells + [text]).lower()
        slash = re.search(r"kr/([a-zåäö0-9³]+)", joined)
        if slash:
            return self.UNIT_ALIASES.get(slash.group(1), slash.group(1))

        for key, value in self.UNIT_ALIASES.items():
            if re.search(rf"\b{re.escape(key)}\b", joined):
                return value

        return ""
