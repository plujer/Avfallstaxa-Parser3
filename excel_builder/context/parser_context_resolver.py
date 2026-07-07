"""Resolve inherited context for parser tax rows.

This module addresses a major remaining quality issue:
many Word rows are structurally meaningful headings or partial tax rows. They
need nearby context before semantic matching can work well.
"""

from __future__ import annotations

from excel_builder.matching import MatchNormalizer
from excel_builder.models import ContextResolutionReport, ContextResolvedTaxRow, ParserTaxContext, ParserTaxRow


class ParserContextResolver:
    SECTION_CONTEXT = {
        "2": "Hushåll",
        "3": "Flerbostad/verksamhet",
        "4": "Tilläggstjänst",
        "5": "Slam",
        "6": "Verksamhetsavfall",
    }

    PROPERTY_PATTERNS = {
        "En- och tvåbostadshus": ["en- och tvåbostad", "en och tvåbostad", "småhus", "smahus", "villa"],
        "Fritidshus": ["fritidshus", "fritidsboende"],
        "Flerbostadshus": ["flerbostad", "lägenhet", "lagenhet"],
        "Verksamhet": ["verksamhet", "företag", "foretag"],
    }

    WASTE_PATTERNS = {
        "Restavfall": ["restavfall", "brännbart", "brannbart"],
        "Matavfall": ["matavfall"],
        "Mat-/restavfall": ["mat-/restavfall", "mat- och restavfall", "mat och restavfall"],
        "Förpackningar": ["förpackning", "förpackningar", "forpackning", "forpackningar"],
        "Slam": ["slam", "slamtömning"],
        "Asbest": ["asbest"],
        "Gips": ["gips"],
        "Träavfall": ["träavfall", "trä", "tra"],
        "Farligt avfall": ["farligt avfall"],
    }

    SERVICE_PATTERNS = {
        "Abonnemang": ["abonnemang", "grundavgift", "årsavgift", "arsavgift"],
        "Hämtning/tömning": ["hämtning", "hamtning", "tömning", "tomning"],
        "Extra": ["extra", "extratömning", "extra tömning"],
        "Utkörning/leverans": ["utställning", "utstallning", "leverans", "hemtransport"],
        "Byte": ["byte", "kärlbyte", "karlsbyte"],
        "Mottagning/behandling": ["mottagning", "behandling", "deponi"],
    }

    CONTAINER_PATTERNS = {
        "Kärl": ["kärl", "karl"],
        "Container": ["container"],
        "Säck": ["säck", "sack"],
        "Brunn": ["brunn", "slambrunn"],
        "Latrin": ["latrin"],
    }

    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def resolve(self, rows: list[ParserTaxRow]) -> ContextResolutionReport:
        report = ContextResolutionReport()
        current_section_context = ""
        current_property_context = ""
        current_waste_context = ""
        current_service_context = ""
        current_container_context = ""

        for idx, row in enumerate(rows, start=1):
            text = self._norm(" ".join([row.section, row.tax_point, row.variant, row.unit]))

            section_context = self._section_context(row.section) or current_section_context
            property_context = self._match_patterns(text, self.PROPERTY_PATTERNS) or current_property_context
            waste_context = self._match_patterns(text, self.WASTE_PATTERNS) or current_waste_context
            service_context = self._match_patterns(text, self.SERVICE_PATTERNS) or current_service_context
            container_context = self._match_patterns(text, self.CONTAINER_PATTERNS) or current_container_context

            # Update rolling context when the current row clearly carries context.
            if section_context:
                current_section_context = section_context
            if self._match_patterns(text, self.PROPERTY_PATTERNS):
                current_property_context = property_context
            if self._match_patterns(text, self.WASTE_PATTERNS):
                current_waste_context = waste_context
            if self._match_patterns(text, self.SERVICE_PATTERNS):
                current_service_context = service_context
            if self._match_patterns(text, self.CONTAINER_PATTERNS):
                current_container_context = container_context

            inherited_parts = [
                section_context,
                property_context,
                waste_context,
                service_context,
                container_context,
            ]
            inherited_text = " ".join([part for part in inherited_parts if part])

            enriched = ParserTaxRow(
                section=row.section,
                tax_point=self._enrich_text(row.tax_point, inherited_text),
                variant=self._enrich_text(row.variant, inherited_text) if row.variant else row.variant,
                unit=row.unit,
            )

            context = ParserTaxContext(
                row_index=idx,
                parser_row=row,
                section_context=section_context,
                property_type_context=property_context,
                waste_type_context=waste_context,
                container_context=container_context,
                service_context=service_context,
                inherited_text=inherited_text,
                confidence=self._confidence(section_context, property_context, waste_context, container_context, service_context),
                notes=self._notes(row, inherited_text),
            )

            report.rows.append(ContextResolvedTaxRow(original_row=row, enriched_row=enriched, context=context))

        return report

    def _section_context(self, section: str) -> str:
        normalized = self.normalizer.normalize_section(section)
        major = normalized.split(".")[0] if normalized else ""
        return self.SECTION_CONTEXT.get(major, "")

    def _match_patterns(self, text: str, patterns: dict[str, list[str]]) -> str:
        for label, needles in patterns.items():
            for needle in needles:
                if self._norm(needle) in text:
                    return label
        return ""

    def _enrich_text(self, text: str, inherited_text: str) -> str:
        if not inherited_text:
            return text

        normalized_text = self._norm(text)
        additions = []
        for part in inherited_text.split():
            if self._norm(part) and self._norm(part) not in normalized_text:
                additions.append(part)

        if not additions:
            return text

        return f"{text} [{' '.join(additions)}]".strip()

    def _confidence(self, *values: str) -> float:
        return min(sum(1 for value in values if value) * 0.18, 0.90)

    def _notes(self, row: ParserTaxRow, inherited_text: str) -> list[str]:
        notes = []
        if inherited_text:
            notes.append("Kontext ärvd från sektion/rubrik/närliggande rader.")
        if len(self._norm(row.tax_point).split()) <= 2:
            notes.append("Kort taxarad – kontext är extra viktig.")
        return notes

    def _norm(self, value: str) -> str:
        return self.normalizer.normalize(value)
