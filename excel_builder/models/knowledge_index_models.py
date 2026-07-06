"""Knowledge index models for rule-based tax matching."""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.knowledge_models import TaxKnowledgeFeature
from excel_builder.models.standard_tax_models import StandardTaxRow


@dataclass(frozen=True)
class KnowledgeIndexKey:
    category: str = ""
    waste_type: str = ""
    unit_type: str = ""
    factor_hint: str = ""
    container_volume_liter: str = ""


@dataclass
class KnowledgeIndexEntry:
    key: KnowledgeIndexKey
    feature_count: int = 0
    standard_rows: list[StandardTaxRow] = field(default_factory=list)
    feature_examples: list[TaxKnowledgeFeature] = field(default_factory=list)


@dataclass
class KnowledgeIndex:
    entries: dict[KnowledgeIndexKey, KnowledgeIndexEntry] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @property
    def entry_count(self) -> int:
        return len(self.entries)

    @property
    def standard_row_count(self) -> int:
        seen: set[tuple[str, int]] = set()
        for entry in self.entries.values():
            for row in entry.standard_rows:
                seen.add((row.source_sheet, row.row_number))
        return len(seen)

    def get_or_create(self, key: KnowledgeIndexKey) -> KnowledgeIndexEntry:
        if key not in self.entries:
            self.entries[key] = KnowledgeIndexEntry(key=key)
        return self.entries[key]
