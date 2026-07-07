"""Resolve hierarchical context for parser tax rows.

Block35 replaces the old rolling context behavior with a document-structure
aware resolver. Context is inherited from explicit SECTION/SUBSECTION parents
created by Document Structure Engine and is reset when a new structural parent
is encountered. The resolver is non-destructive: original parser rows are kept
and Taxa_från_edp is never modified.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.document import DocumentStructureEngine
from excel_builder.matching import MatchNormalizer
from excel_builder.models import (
    ContextResolutionReport,
    ContextResolvedTaxRow,
    DocumentRowType,
    DocumentStructureNode,
    ParserTaxContext,
    ParserTaxRow,
)


@dataclass
class _HierarchyState:
    section_node: DocumentStructureNode | None = None
    subsection_node: DocumentStructureNode | None = None
    section_context: str = ""
    property_context: str = ""
    waste_context: str = ""
    service_context: str = ""
    container_context: str = ""
    structure_texts: list[str] = field(default_factory=list)

    def path(self) -> str:
        return " > ".join(text for text in self.structure_texts if text)

    def inherited_parts(self) -> list[str]:
        parts = [
            self.section_context,
            self.property_context,
            self.waste_context,
            self.service_context,
            self.container_context,
        ]
        return [part for part in parts if part]


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
        "Anläggning": ["anläggning", "anlaggning"],
        "Camping": ["camping"],
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
        "Jord": ["jord"],
        "Sten": ["sten"],
        "Fönster": ["fönster", "fonster"],
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
        self.structure_engine = DocumentStructureEngine()

    def resolve(self, rows: list[ParserTaxRow]) -> ContextResolutionReport:
        report = ContextResolutionReport()
        structure = self.structure_engine.classify(rows)
        state = _HierarchyState()

        for node in structure.nodes:
            if node.row_type == DocumentRowType.SECTION:
                state = self._start_section(node)
                continue

            if node.row_type == DocumentRowType.SUBSECTION:
                state = self._start_subsection(state, node)
                continue

            if node.row_type not in {DocumentRowType.TAX_NODE, DocumentRowType.TABLE_ROW}:
                continue

            resolved = self._resolve_tax_node(node, state)
            report.rows.append(resolved)

        return report

    def _start_section(self, node: DocumentStructureNode) -> _HierarchyState:
        section_context = self._section_context(node.parser_row.section)
        structure_name = node.parser_row.tax_point.strip()
        next_state = _HierarchyState(
            section_node=node,
            subsection_node=None,
            section_context=section_context,
            structure_texts=[structure_name] if structure_name else [],
        )
        self._merge_context_from_text(next_state, self._node_text(node), replace=True)
        return next_state

    def _start_subsection(self, state: _HierarchyState, node: DocumentStructureNode) -> _HierarchyState:
        structure_name = node.parser_row.tax_point.strip()
        # New subsection inherits the active section only. Lower-level context is
        # reset first so property/waste labels cannot leak across sibling blocks.
        next_state = _HierarchyState(
            section_node=state.section_node,
            subsection_node=node,
            section_context=state.section_context or self._section_context(node.parser_row.section),
            structure_texts=([state.structure_texts[0]] if state.section_node and state.structure_texts else []) + ([structure_name] if structure_name else []),
        )
        self._merge_context_from_text(next_state, self._node_text(node), replace=True)
        return next_state

    def _resolve_tax_node(self, node: DocumentStructureNode, state: _HierarchyState) -> ContextResolvedTaxRow:
        row = node.parser_row
        local_text = self._row_text(row)

        resolved_state = _HierarchyState(
            section_node=state.section_node,
            subsection_node=state.subsection_node,
            section_context=state.section_context or self._section_context(row.section),
            property_context=state.property_context,
            waste_context=state.waste_context,
            service_context=state.service_context,
            container_context=state.container_context,
            structure_texts=list(state.structure_texts),
        )
        self._merge_context_from_text(resolved_state, local_text, replace=False)

        inherited_text = " ".join(resolved_state.inherited_parts())
        enriched = ParserTaxRow(
            section=row.section,
            tax_point=self._enrich_text(row.tax_point, inherited_text),
            variant=self._enrich_text(row.variant, inherited_text) if row.variant else row.variant,
            unit=row.unit,
            price=row.price,
        )

        context = ParserTaxContext(
            row_index=node.row_index,
            parser_row=row,
            section_context=resolved_state.section_context,
            property_type_context=resolved_state.property_context,
            waste_type_context=resolved_state.waste_context,
            container_context=resolved_state.container_context,
            service_context=resolved_state.service_context,
            inherited_text=inherited_text,
            hierarchy_path=resolved_state.path(),
            parent_structure_index=(resolved_state.subsection_node or resolved_state.section_node).row_index if (resolved_state.subsection_node or resolved_state.section_node) else None,
            confidence=self._confidence(
                resolved_state.section_context,
                resolved_state.property_context,
                resolved_state.waste_context,
                resolved_state.container_context,
                resolved_state.service_context,
            ),
            notes=self._notes(row, inherited_text, resolved_state.path()),
        )
        return ContextResolvedTaxRow(original_row=row, enriched_row=enriched, context=context)

    def _merge_context_from_text(self, state: _HierarchyState, text: str, replace: bool) -> None:
        property_context = self._match_patterns(text, self.PROPERTY_PATTERNS)
        waste_context = self._match_patterns(text, self.WASTE_PATTERNS)
        service_context = self._match_patterns(text, self.SERVICE_PATTERNS)
        container_context = self._match_patterns(text, self.CONTAINER_PATTERNS)

        if property_context or replace:
            state.property_context = property_context if property_context else state.property_context
        if waste_context or replace:
            state.waste_context = waste_context if waste_context else state.waste_context
        if service_context or replace:
            state.service_context = service_context if service_context else state.service_context
        if container_context or replace:
            state.container_context = container_context if container_context else state.container_context

    def _section_context(self, section: str) -> str:
        normalized = self.normalizer.normalize_section(section)
        major = normalized.split(".")[0] if normalized else ""
        return self.SECTION_CONTEXT.get(major, "")

    def _match_patterns(self, text: str, patterns: dict[str, list[str]]) -> str:
        normalized = self._norm(text)
        for label, needles in patterns.items():
            for needle in needles:
                if self._norm(needle) in normalized:
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

    def _notes(self, row: ParserTaxRow, inherited_text: str, hierarchy_path: str) -> list[str]:
        notes = []
        if inherited_text:
            notes.append("Kontext ärvd från dokumenthierarki/strukturrubriker.")
        if hierarchy_path:
            notes.append(f"Hierarki: {hierarchy_path}")
        if len(self._norm(row.tax_point).split()) <= 2:
            notes.append("Kort taxarad – hierarkisk kontext är extra viktig.")
        return notes

    def _node_text(self, node: DocumentStructureNode) -> str:
        return self._row_text(node.parser_row)

    def _row_text(self, row: ParserTaxRow) -> str:
        return " ".join([row.section, row.tax_point, row.variant, row.unit])

    def _norm(self, value: str) -> str:
        return self.normalizer.normalize(value)
