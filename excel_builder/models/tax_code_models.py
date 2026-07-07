"""Tax code intelligence models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ParsedTaxCode:
    original_code: str
    prefix: str = ""
    container_type: str = ""
    volume_liter: str = ""
    waste_code: str = ""
    waste_type: str = ""
    interval: str = ""
    variant: str = ""
    suffix: str = ""
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def family_key(self) -> str:
        parts = [self.prefix, self.volume_liter, self.waste_code]
        return "".join([part for part in parts if part])


@dataclass
class TaxCodeParseReport:
    parsed_codes: list[ParsedTaxCode] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.parsed_codes)

    @property
    def parsed_with_family(self) -> int:
        return sum(1 for item in self.parsed_codes if item.family_key)
