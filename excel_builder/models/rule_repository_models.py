"""Rule repository models built from the master workbook.

The rule repository is global knowledge. It may be reused across projects, but
it must not mix municipality-specific EDP exports between projects.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MasterRule:
    source_sheet: str
    row_number: int
    rule_type: str
    priority: int = 100
    section: str = ""
    tax_point: str = ""
    category: str = ""
    waste_type: str = ""
    unit_type: str = ""
    factor_hint: str = ""
    container_volume_liter: str = ""
    tax_code: str = ""
    standard_tax_code: str = ""
    formula: str = ""
    tax_part: str = ""
    source_text: str = ""
    confidence: float = 0.0


@dataclass
class RuleRepository:
    source_workbook: str
    rules: list[MasterRule] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def rule_count(self) -> int:
        return len(self.rules)

    def by_type(self, rule_type: str) -> list[MasterRule]:
        return [rule for rule in self.rules if rule.rule_type == rule_type]

    @property
    def edp_rules(self) -> list[MasterRule]:
        return self.by_type("EDP")

    @property
    def taxepunkt_rules(self) -> list[MasterRule]:
        return self.by_type("TAXEPUNKT")

    @property
    def documentation_rules(self) -> list[MasterRule]:
        return self.by_type("DOCUMENTATION")
