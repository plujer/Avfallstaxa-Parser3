"""Build semantic attribute profiles from standard catalog and master rules."""

from __future__ import annotations

from excel_builder.models import RuleRepository, SemanticAttributeReport, StandardTaxCatalog
from excel_builder.semantic_attributes.attribute_extractor import SemanticAttributeExtractor


class SemanticAttributeRepository:
    def __init__(self) -> None:
        self.extractor = SemanticAttributeExtractor()

    def from_standard_and_rules(self, catalog: StandardTaxCatalog, repo: RuleRepository) -> SemanticAttributeReport:
        report = SemanticAttributeReport()
        seen: set[tuple[str, str]] = set()

        for row in catalog.rows:
            code = str(row.strTaxekod or "").strip()
            text = " ".join(
                part for part in [row.strTaxebenamning, row.strFaktor, row.strTaxedelAvser, row.strFormel] if part
            )
            source = f"STANDARD:{row.source_sheet}:{row.row_number}"
            profile = self.extractor.extract(code, text, source)
            key = (profile.tax_code, profile.source)
            if key not in seen:
                seen.add(key)
                report.profiles.append(profile)

        for rule in repo.rules:
            code = str(rule.tax_code or rule.standard_tax_code or "").strip()
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
            source = f"RULE:{rule.source_sheet}:{rule.row_number}"
            profile = self.extractor.extract(code, text, source)
            key = (profile.tax_code, profile.source)
            if key not in seen:
                seen.add(key)
                report.profiles.append(profile)

        for profile in report.profiles:
            if profile.source_text and profile.attribute_count == 0:
                report.warnings.append(f"Inga semantiska attribut hittades för {profile.source}")

        return report
