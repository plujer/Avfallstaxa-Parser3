"""Semantic parser using ContextEngine and unified extraction."""

from __future__ import annotations

from dataclasses import dataclass, field

from parser3.context.context_engine import ContextEngine
from parser3.document import DocumentBlock
from parser3.extractors import FlatTaxExtractor, Section611Extractor, Section612Extractor, Section614Extractor, TaxRowExtractor
from parser3.models import TaxRow
from parser3.semantic.row_type_classifier import RowTypeClassifier
from parser3.semantic.section_tax_rules import SectionTaxRules
from parser3.semantic.semantic_row import SemanticRow
from parser3.tables2 import StructuredTaxExtractor
from parser3.trace import TraceStore
from parser3.utils.constants import ROW_TYPE_TAX


@dataclass
class SemanticParseResult:
    semantic_rows: list[SemanticRow] = field(default_factory=list)
    tax_rows: list[TaxRow] = field(default_factory=list)
    trace_store: TraceStore = field(default_factory=TraceStore)


class SemanticParser:
    def __init__(self, trace_store: TraceStore | None = None) -> None:
        self.trace_store = trace_store or TraceStore()
        self.context_engine = ContextEngine()
        self.row_classifier = RowTypeClassifier()
        self.section_rules = SectionTaxRules()
        self.tax_extractor = TaxRowExtractor()
        self.flat_extractor = FlatTaxExtractor()
        self.structured_extractor = StructuredTaxExtractor()
        self.section612_extractor = Section612Extractor(trace_store=self.trace_store)
        self.section611_extractor = Section611Extractor()
        self.section614_extractor = Section614Extractor()

    def parse(self, blocks: list[DocumentBlock]) -> SemanticParseResult:
        context_blocks = self.context_engine.assign(blocks)
        semantic_rows: list[SemanticRow] = []
        tax_rows: list[TaxRow] = []
        seen_keys: set[tuple[str, str, str, str]] = set()
        pending_611_text = ""
        pending_614_text = ""

        def add_rows(new_rows: list[TaxRow]) -> None:
            for row in new_rows:
                # §6.1.3 contains three visually identical Container X m³ rows.
                # They must remain three export rows.
                if row.section == "6.1.3":
                    tax_rows.append(row)
                    continue

                key = (row.section, row.name, row.variant, row.unit)
                if key not in seen_keys:
                    seen_keys.add(key)
                    tax_rows.append(row)

        for context_block in context_blocks:
            block = context_block.block
            context = context_block.context

            if context.section != "6.1.1":
                pending_611_text = ""
            if context.section != "6.1.4":
                pending_614_text = ""

            if block.kind == "table":
                for index, row in enumerate(block.rows):
                    row_context = context_block.row_contexts[index] if index < len(context_block.row_contexts) else context
                    row_type, reason = self.row_classifier.classify(row)
                    text = " ".join(c for c in row if c).strip()
                    semantic_rows.append(
                        SemanticRow(
                            row_type=row_type,
                            text=text,
                            cells=row,
                            order=block.order,
                            section=row_context.section,
                            group=row_context.group,
                            reason=reason,
                        )
                    )

                    if row_context.section == "6.1.2" and row_type != ROW_TYPE_TAX:
                        add_rows(
                            self.section612_extractor.extract_line(
                                text,
                                chapter=row_context.chapter,
                                section=row_context.section,
                                group=row_context.group,
                                order=block.order,
                            )
                        )

                if self.section_rules.should_export(context.section, "table"):
                    if any(len([c for c in row if (c or '').strip()]) > 1 for row in block.rows):
                        add_rows(
                            self.structured_extractor.extract_table(
                                block.rows,
                                chapter=context.chapter,
                                section=context.section,
                                group=context.group,
                            )
                        )
                    else:
                        for row in block.rows:
                            text = " ".join(c for c in row if c).strip()
                            add_rows(
                                self.flat_extractor.extract_line(
                                    text,
                                    chapter=context.chapter,
                                    section=context.section,
                                    group=context.group,
                                )
                            )
                continue

            row_type, reason = self.row_classifier.classify([block.text])
            semantic_rows.append(
                SemanticRow(
                    row_type="section" if context.section and block.text.startswith(context.section) else row_type,
                    text=block.text,
                    cells=[block.text],
                    order=block.order,
                    section=context.section,
                    group=context.group,
                    reason=reason,
                )
            )

            if context.section == "6.1.1":
                if pending_611_text and row_type == ROW_TYPE_TAX:
                    add_rows(
                        self.section611_extractor.extract_combined(
                            pending_611_text,
                            block.text,
                            chapter=context.chapter,
                            section=context.section,
                            group=context.group,
                        )
                    )

                if block.text.strip().lower().startswith("ej redovisad ankomst till åvc"):
                    pending_611_text = block.text
                elif row_type == ROW_TYPE_TAX:
                    pending_611_text = ""

            if context.section == "6.1.4":
                if pending_614_text and row_type == ROW_TYPE_TAX:
                    add_rows(
                        self.section614_extractor.extract_combined(
                            pending_614_text,
                            block.text,
                            chapter=context.chapter,
                            section=context.section,
                            group=context.group,
                        )
                    )

                if block.text.strip().lower().startswith("ombud för registrering av el-kretsen"):
                    pending_614_text = block.text
                elif row_type == ROW_TYPE_TAX:
                    pending_614_text = ""

            if context.section == "6.1.2" and row_type != ROW_TYPE_TAX:
                add_rows(
                    self.section612_extractor.extract_line(
                        block.text,
                        chapter=context.chapter,
                        section=context.section,
                        group=context.group,
                        order=block.order,
                    )
                )

            if row_type == ROW_TYPE_TAX and self.section_rules.should_export(context.section, block.text):
                add_rows(
                    self.flat_extractor.extract_line(
                        block.text,
                        chapter=context.chapter,
                        section=context.section,
                        group=context.group,
                    )
                )

        return SemanticParseResult(semantic_rows=semantic_rows, tax_rows=tax_rows, trace_store=self.trace_store)
