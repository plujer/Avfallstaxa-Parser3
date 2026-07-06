"""Semantic parser using ContextEngine and unified extraction."""

from __future__ import annotations

from dataclasses import dataclass, field

from parser3.context.context_engine import ContextEngine
from parser3.document import DocumentBlock
from parser3.extractors import FlatTaxExtractor, TaxRowExtractor
from parser3.models import TaxRow
from parser3.semantic.row_type_classifier import RowTypeClassifier
from parser3.semantic.section_tax_rules import SectionTaxRules
from parser3.semantic.semantic_row import SemanticRow
from parser3.tables2 import StructuredTaxExtractor
from parser3.utils.constants import ROW_TYPE_TAX


@dataclass
class SemanticParseResult:
    semantic_rows: list[SemanticRow] = field(default_factory=list)
    tax_rows: list[TaxRow] = field(default_factory=list)


class SemanticParser:
    def __init__(self) -> None:
        self.context_engine = ContextEngine()
        self.row_classifier = RowTypeClassifier()
        self.section_rules = SectionTaxRules()
        self.tax_extractor = TaxRowExtractor()
        self.flat_extractor = FlatTaxExtractor()
        self.structured_extractor = StructuredTaxExtractor()

    def parse(self, blocks: list[DocumentBlock]) -> SemanticParseResult:
        context_blocks = self.context_engine.assign(blocks)
        semantic_rows: list[SemanticRow] = []
        tax_rows: list[TaxRow] = []

        for context_block in context_blocks:
            block = context_block.block
            context = context_block.context

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

                if self.section_rules.should_export(context.section, "table"):
                    # Native multi-cell tables use StructuredTaxExtractor.
                    if any(len([c for c in row if (c or '').strip()]) > 1 for row in block.rows):
                        tax_rows.extend(
                            self.structured_extractor.extract_table(
                                block.rows,
                                chapter=context.chapter,
                                section=context.section,
                                group=context.group,
                            )
                        )
                    else:
                        # Visual tables stored as one-cell rows use FlatTaxExtractor.
                        for row in block.rows:
                            text = " ".join(c for c in row if c).strip()
                            tax_rows.extend(
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

            if row_type == ROW_TYPE_TAX and self.section_rules.should_export(context.section, block.text):
                tax_rows.extend(
                    self.flat_extractor.extract_line(
                        block.text,
                        chapter=context.chapter,
                        section=context.section,
                        group=context.group,
                    )
                )

        return SemanticParseResult(semantic_rows=semantic_rows, tax_rows=tax_rows)
