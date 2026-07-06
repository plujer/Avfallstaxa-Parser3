"""Section-specific tax extraction rules."""

from __future__ import annotations


class SectionTaxRules:
    SECTION_COUNTS = {
        "6.1.1": 6,
        "6.1.2": 103,
        "6.1.3": 4,
        "6.1.4": 4,
    }

    def expected_count(self, section: str) -> int | None:
        return self.SECTION_COUNTS.get(section)

    def should_export(self, section: str, text: str) -> bool:
        lower = (text or "").lower()

        # Chapter 1 contains definitions and legal text, not exportable tax rows.
        if not section or section.startswith("1"):
            return False

        if section == "6.1.2" and "toner" in lower and "utan elektronik" in lower and "se farligt avfall" in lower:
            return False

        # Section headings must never export.
        if "§" in lower and lower.strip()[0:1].isdigit():
            return False

        return True

    def normalize_group(self, text: str, current_group: str = "") -> str:
        lower = (text or "").lower()
        if "tillägg för farligt avfall" in lower:
            return "Tillägg för farligt avfall"
        if "tillägg för el-avfall" in lower:
            return "Tillägg för el-avfall"
        if "övriga avgifter" in lower:
            return "Övriga avgifter"
        return current_group
