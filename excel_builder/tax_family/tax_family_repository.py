"""Build and query tax-code family repositories."""

from __future__ import annotations

from collections import defaultdict

from excel_builder.models import RuleRepository, StandardTaxCatalog, TaxFamily, TaxFamilyReport
from excel_builder.tax_family.tax_family_parser import TaxFamilyParser


class TaxFamilyRepository:
    def __init__(self) -> None:
        self.parser = TaxFamilyParser()

    def from_codes(self, codes: list[str], source: str = "") -> TaxFamilyReport:
        buckets = defaultdict(list)
        report = TaxFamilyReport()

        for code in sorted({str(code or "").strip() for code in codes if str(code or "").strip()}):
            member = self.parser.parse_member(code, source=source)
            family_code = member.family_key.value
            if not family_code:
                report.warnings.append(f"Ingen familj kunde identifieras för taxekod: {code}")
                continue
            buckets[family_code].append(member)

        for family_code in sorted(buckets):
            first = buckets[family_code][0]
            report.families.append(TaxFamily(key=first.family_key, members=buckets[family_code]))

        return report

    def from_standard_and_rules(self, catalog: StandardTaxCatalog, repo: RuleRepository) -> TaxFamilyReport:
        codes: list[str] = []

        for row in catalog.rows:
            if row.strTaxekod:
                codes.append(row.strTaxekod)

        for rule in repo.rules:
            if rule.tax_code:
                codes.append(rule.tax_code)
            if rule.standard_tax_code:
                codes.append(rule.standard_tax_code)

        return self.from_codes(codes, source="STANDARD+RULES")
