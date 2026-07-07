"""Build semantic profiles for tax rows from different sources."""

from __future__ import annotations

import re

from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.matching import MatchNormalizer
from excel_builder.models import (
    MasterRule,
    ParserTaxRow,
    RuleRepository,
    StandardTaxCatalog,
    StandardTaxRow,
    TaxKnowledgeFeature,
    TaxKnowledgeReport,
    TaxSemanticProfile,
    TaxSemanticProfileKey,
    TaxSemanticProfileReport,
)


class TaxSemanticProfileEngine:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()
        self.knowledge_extractor = TaxKnowledgeExtractor()

    def from_knowledge_report(self, knowledge_report: TaxKnowledgeReport) -> TaxSemanticProfileReport:
        report = TaxSemanticProfileReport()
        report.warnings.extend(knowledge_report.warnings)

        for idx, feature in enumerate(knowledge_report.features, start=1):
            report.profiles.append(self.from_feature(feature, source_id=f"WORD:{idx}"))

        return report

    def from_standard_catalog(self, catalog: StandardTaxCatalog) -> TaxSemanticProfileReport:
        report = TaxSemanticProfileReport()
        report.warnings.extend(catalog.warnings)

        for row in catalog.rows:
            report.profiles.append(self.from_standard_row(row))

        return report

    def from_rule_repository(self, repo: RuleRepository) -> TaxSemanticProfileReport:
        report = TaxSemanticProfileReport()
        report.warnings.extend(repo.warnings)

        for rule in repo.rules:
            report.profiles.append(self.from_master_rule(rule))

        return report

    def from_feature(self, feature: TaxKnowledgeFeature, source_id: str = "") -> TaxSemanticProfile:
        text = self._norm(" ".join([
            feature.parser_row.section,
            feature.parser_row.tax_point,
            feature.parser_row.variant,
            feature.parser_row.unit,
            " ".join(feature.keywords),
        ]))
        key = TaxSemanticProfileKey(
            category=feature.category,
            waste_type=feature.waste_type,
            service_type=self._service_type(text),
            container_type=self._container_type(text),
            container_volume_liter=feature.container_volume_liter or self._container_volume(text),
            interval=self._interval(text),
            property_type=self._property_type(text),
            unit_type=feature.unit_type,
            factor_hint=feature.factor_hint,
        )
        return TaxSemanticProfile(
            source="WORD",
            source_id=source_id or f"{feature.parser_row.section}:{feature.parser_row.tax_point}",
            key=key,
            source_text=text,
            confidence=feature.confidence,
            keywords=feature.keywords,
            notes=feature.notes,
        )

    def from_standard_row(self, row: StandardTaxRow) -> TaxSemanticProfile:
        text = self._norm(" ".join([
            row.source_sheet,
            row.strTaxekod,
            row.strTaxebenamning,
            row.strFaktor,
            row.strTaxedelAvser,
            row.strFormel,
        ]))
        feature = self.knowledge_extractor.extract([
            ParserTaxRow(section="", tax_point=row.strTaxebenamning, variant="", unit=row.strTaxedelAvser)
        ]).features[0]

        key = TaxSemanticProfileKey(
            category=self._category_from_standard(row.source_sheet, text) or feature.category,
            waste_type=feature.waste_type,
            service_type=self._service_type(text),
            container_type=self._container_type(text),
            container_volume_liter=feature.container_volume_liter or self._container_volume(text),
            interval=self._interval(text),
            property_type=self._property_type(text),
            unit_type=feature.unit_type,
            factor_hint=row.strFaktor or feature.factor_hint,
        )

        return TaxSemanticProfile(
            source="STANDARD",
            source_id=f"{row.source_sheet}:{row.row_number}",
            key=key,
            source_text=text,
            tax_code=row.strTaxekod,
            standard_tax_code=row.strTaxekod,
            confidence=0.80,
            keywords=feature.keywords,
        )

    def from_master_rule(self, rule: MasterRule) -> TaxSemanticProfile:
        text = self._norm(" ".join([
            rule.section,
            rule.tax_point,
            rule.source_text,
            rule.tax_code,
            rule.formula,
            rule.tax_part,
        ]))
        key = TaxSemanticProfileKey(
            category=rule.category,
            waste_type=rule.waste_type,
            service_type=self._service_type(text),
            container_type=self._container_type(text),
            container_volume_liter=rule.container_volume_liter or self._container_volume(text),
            interval=self._interval(text),
            property_type=self._property_type(text),
            unit_type=rule.unit_type,
            factor_hint=rule.factor_hint,
        )

        return TaxSemanticProfile(
            source=f"RULE:{rule.rule_type}",
            source_id=f"{rule.source_sheet}:{rule.row_number}",
            key=key,
            source_text=text,
            tax_code=rule.tax_code,
            standard_tax_code=rule.standard_tax_code,
            confidence=rule.confidence,
        )

    def _category_from_standard(self, source_sheet: str, text: str) -> str:
        source = self._norm(source_sheet)
        if "slam" in source or "slam" in text:
            return "Slam"
        if "avfall" in source:
            return "ÅVC/verksamhetsavfall"
        if "åvs" in source or "avs" in source:
            return "ÅVS"
        return ""

    def _service_type(self, text: str) -> str:
        if any(word in text for word in ["extra", "extratömning", "extra tömning"]):
            return "Extra"
        if any(word in text for word in ["hämtning", "hamtning", "tömning", "tomning", "slamtömning"]):
            return "Hämtning/tömning"
        if any(word in text for word in ["utställning", "utstallning", "hemtransport", "leverans"]):
            return "Utkörning/leverans"
        if any(word in text for word in ["byte", "kärlbyte", "karlsbyte"]):
            return "Byte"
        if any(word in text for word in ["abonnemang", "år", "ar", "grundavgift"]):
            return "Abonnemang"
        if any(word in text for word in ["behandling", "mottagning", "deponi"]):
            return "Mottagning/behandling"
        return ""

    def _container_type(self, text: str) -> str:
        if "kärl" in text or "karl" in text:
            return "Kärl"
        if "container" in text:
            return "Container"
        if "säck" in text or "sack" in text:
            return "Säck"
        if "slambrunn" in text or "brunn" in text:
            return "Brunn"
        if "latrin" in text:
            return "Latrin"
        return ""

    def _container_volume(self, text: str) -> str:
        match = re.search(r"\b(\d{2,4})\s*l\b", text)
        if match:
            return match.group(1)
        match = re.search(r"\b(\d{2,4})\s*liter\b", text)
        if match:
            return match.group(1)
        match = re.search(r"\b(\d{1,3})\s*m3\b", text)
        if match:
            return f"{match.group(1)}m3"
        return ""

    def _interval(self, text: str) -> str:
        patterns = [
            (r"\b(\d+)\s*ggr?\s*/\s*år\b", r"\1 ggr/år"),
            (r"\b(\d+)\s*gånger\s*per\s*år\b", r"\1 ggr/år"),
            (r"\bvar\s*(\d+)\s*e?\s*vecka\b", r"var \1 vecka"),
            (r"\bvarannan\s*vecka\b", "varannan vecka"),
            (r"\bvecko", "varje vecka"),
            (r"\bmånad\b", "månad"),
        ]
        for pattern, repl in patterns:
            match = re.search(pattern, text)
            if match:
                if "\\" in repl:
                    return match.expand(repl)
                return repl
        return ""

    def _property_type(self, text: str) -> str:
        if "fritid" in text or "fritidshus" in text:
            return "Fritidshus"
        if "villa" in text or "småhus" in text or "smahus" in text:
            return "Villa/småhus"
        if "flerbostad" in text or "lägenhet" in text or "lagenhet" in text:
            return "Flerbostadshus"
        if "verksamhet" in text or "företag" in text or "foretag" in text:
            return "Verksamhet"
        return ""

    def _norm(self, value: str) -> str:
        return self.normalizer.normalize(value)
