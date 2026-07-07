"""Document Structure Engine for parser rows.

Block34 goal: classify parser rows as structure or real tax nodes so headings
such as "En- och tvåbostadshus" and "Fritidshus" do not become NEW_TAXA.
"""

from __future__ import annotations

import re

from excel_builder.matching import MatchNormalizer
from excel_builder.models import ParserTaxRow
from excel_builder.models.document_structure_models import (
    DocumentRowType,
    DocumentStructureNode,
    DocumentStructureReport,
)


class DocumentStructureEngine:
    """Classify parser rows and build a shallow parent/child structure."""

    STRUCTURAL_HEADINGS = {
        "en- och tvåbostadshus",
        "en-och tvåbostadshus",
        "en och tvåbostadshus",
        "fritidshus",
        "verksamhet",
        "lägenhet i flerbostadshus",
        "lagenhet i flerbostadshus",
        "lägenhet för specialändamål",
        "lagenhet for specialandamal",
        "anläggning",
        "anlaggning",
        "säsongsbaserad uppställningsplats",
        "sasongsbaserad uppstallningsplats",
        "campingstuga/-lägenhet",
        "campingstuga lagenhet",
    }

    TABLE_HEADER_TERMS = {
        "taxa",
        "benämning",
        "benamning",
        "avgift",
        "pris",
        "enhet",
        "kr",
        "kronor",
    }

    NOTE_PREFIXES = (
        "anm",
        "anmärkning",
        "anmarkning",
        "not",
        "obs",
        "information",
        "definition",
        "avser",
    )

    TAX_TERMS = (
        "kärl",
        "karl",
        "säck",
        "sack",
        "container",
        "latrin",
        "slam",
        "tömning",
        "tomning",
        "hämtning",
        "hamtning",
        "extra",
        "byte",
        "leverans",
        "mottagning",
        "behandling",
        "asbest",
        "gips",
        "deponi",
        "restavfall",
        "matavfall",
        "förpackning",
        "forpackning",
    )

    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def classify(self, rows: list[ParserTaxRow]) -> DocumentStructureReport:
        report = DocumentStructureReport()
        current_section_parent: int | None = None
        current_subsection_parent: int | None = None

        for idx, row in enumerate(rows, start=1):
            row_type, confidence, reason = self._classify_row(row)
            level = self._level(row, row_type)

            if row_type == DocumentRowType.SECTION:
                current_section_parent = idx
                current_subsection_parent = None
                parent_index = None
            elif row_type == DocumentRowType.SUBSECTION:
                current_subsection_parent = idx
                parent_index = current_section_parent
            else:
                parent_index = current_subsection_parent or current_section_parent

            report.nodes.append(
                DocumentStructureNode(
                    row_index=idx,
                    row_type=row_type,
                    parser_row=row,
                    parent_index=parent_index,
                    level=level,
                    confidence=confidence,
                    reason=reason,
                )
            )

        return report

    def filter_tax_nodes(self, rows: list[ParserTaxRow]) -> list[ParserTaxRow]:
        return self.classify(rows).tax_rows

    def _classify_row(self, row: ParserTaxRow) -> tuple[DocumentRowType, float, str]:
        text = self._norm(" ".join([row.tax_point, row.variant, row.unit]))
        name = self._norm(row.tax_point)
        section = str(row.section or "").strip()
        has_price = bool(str(row.price or "").strip())
        has_unit = bool(str(row.unit or "").strip())

        if not name:
            return DocumentRowType.NOTE, 0.80, "Tom rad utan taxenamn."

        if name in self.STRUCTURAL_HEADINGS:
            return DocumentRowType.SUBSECTION, 0.96, "Känd dokumentrubrik/fastighetstyp, inte taxepunkt."

        if self._looks_like_table_header(text):
            return DocumentRowType.TABLE_HEADER, 0.90, "Tabellrubrik med pris/enhet/avgiftstermer."

        if self._looks_like_note(text):
            return DocumentRowType.NOTE, 0.86, "Informations- eller anmärkningsrad."

        if self._looks_like_section_heading(section, name, has_unit, has_price):
            return DocumentRowType.SECTION, 0.82, "Kort rubrikrad utan enhet/pris/taxetermer."

        if has_unit or self._contains_tax_term(text) or self._contains_volume(text) or has_price:
            return DocumentRowType.TAX_NODE, 0.86, "Rad innehåller taxeterm, enhet, volym eller pris."

        if len(name.split()) <= 3:
            return DocumentRowType.SUBSECTION, 0.72, "Kort rad utan tydlig taxa behandlas som struktur."

        return DocumentRowType.TAX_NODE, 0.55, "Okänd längre rad behålls som möjlig taxepunkt."

    def _looks_like_section_heading(self, section: str, name: str, has_unit: bool, has_price: bool) -> bool:
        if has_unit or has_price:
            return False
        return bool(re.fullmatch(r"\d+(?:\.\d+)*", section)) and len(name.split()) <= 5 and not self._contains_tax_term(name)

    def _looks_like_table_header(self, text: str) -> bool:
        terms = sum(1 for term in self.TABLE_HEADER_TERMS if term in text)
        return terms >= 2 and not self._contains_volume(text)

    def _looks_like_note(self, text: str) -> bool:
        return any(text.startswith(prefix) for prefix in self.NOTE_PREFIXES)

    def _contains_tax_term(self, text: str) -> bool:
        return any(term in text for term in self.TAX_TERMS)

    def _contains_volume(self, text: str) -> bool:
        return bool(re.search(r"\b\d+\s*(?:l|liter|m3|m³|kg|ton)\b", text))

    def _level(self, row: ParserTaxRow, row_type: DocumentRowType) -> int:
        if row_type == DocumentRowType.SECTION:
            return 1
        if row_type == DocumentRowType.SUBSECTION:
            return 2
        if row_type == DocumentRowType.TABLE_HEADER:
            return 3
        return 4

    def _norm(self, value: str) -> str:
        return self.normalizer.normalize(value)
