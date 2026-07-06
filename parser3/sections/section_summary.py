from collections import Counter
from dataclasses import dataclass
from parser3.models import TaxRow

@dataclass
class SectionSummary:
    section: str
    tax_count: int

class SectionSummaryBuilder:
    def build(self, rows: list[TaxRow]) -> list[SectionSummary]:
        counts = Counter(row.section for row in rows if row.export)
        return [SectionSummary(section=s, tax_count=c) for s, c in sorted(counts.items())]
