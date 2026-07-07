"""Build variant profiles from standard catalog and master rules."""

from __future__ import annotations

from excel_builder.models import RuleRepository, StandardTaxCatalog, VariantIntelligenceReport
from excel_builder.variant_intelligence.variant_parser import VariantParser


class VariantRepository:
    def __init__(self) -> None:
        self.parser = VariantParser()

    def from_standard_and_rules(self, catalog: StandardTaxCatalog, repo: RuleRepository) -> VariantIntelligenceReport:
        report = VariantIntelligenceReport()
        seen: set[tuple[str, str]] = set()

        for row in catalog.rows:
            code = str(row.strTaxekod or "").strip()
            if not code:
                continue
            text = " ".join(
                part for part in [row.strTaxebenamning, row.strFaktor, row.strTaxedelAvser, row.strFormel] if part
            )
            profile = self.parser.parse(code, text, source=f"STANDARD:{row.source_sheet}:{row.row_number}")
            key = (profile.tax_code, profile.source)
            if key not in seen:
                seen.add(key)
                report.profiles.append(profile)

        for rule in repo.rules:
            code = str(rule.tax_code or rule.standard_tax_code or "").strip()
            if not code:
                continue
            text = " ".join(
                part
                for part in [
                    rule.tax_point,
                    rule.category,
                    rule.waste_type,
                    rule.unit_type,
                    rule.factor_hint,
                    rule.container_volume_liter,
                    rule.source_text,
                ]
                if part
            )
            profile = self.parser.parse(code, text, source=f"RULE:{rule.source_sheet}:{rule.row_number}")
            key = (profile.tax_code, profile.source)
            if key not in seen:
                seen.add(key)
                report.profiles.append(profile)

        for profile in report.profiles:
            if profile.tax_code and not profile.family_code:
                report.warnings.append(f"Ingen familj kunde identifieras för taxekod: {profile.tax_code}")

        return report
