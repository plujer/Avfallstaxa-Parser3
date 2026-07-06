"""Semantic parser using ContextEngine."""

from __future__ import annotations

from dataclasses import dataclass, field

from parser3.context import ContextEngine
from parser3.document import DocumentBlock
from parser3.extractors import TaxRowExtractor
from parser3.models import TaxRow
from parser3.semantic.row_type_classifier import RowTypeClassifier
from parser3.semantic.section_tax_rules import SectionTaxRules
from parser3.semantic.semantic_row import SemanticRow
from parser3.tables import SmartTableDetector
from parser3.utils.constants import ROW_TYPE_GROUP, ROW_TYPE_HEADER, ROW_TYPE_REFERENCE, ROW_TYPE_TAX


@dataclass
class SemanticParseResult:
    semantic_rows: list[SemanticRow] = field(default_factory=list)
    tax_rows: list[TaxRow] = field(default_factory=list)


class SemanticParser:
    def __init__(self) -> None:
        self.context_engine = ContextEngine()
        self.row_classifier = RowTypeClassifier()
        self.section_rules = SectionTaxRules()
        self.table_detector = SmartTableDetector()
        self.tax_extractor = TaxRowExtractor()

    def parse(self, blocks: list[DocumentBlock]) -> SemanticParseResult:
        context_blocks = self.context_engine.assign(blocks)
        semantic_rows: list[SemanticRow] = []
        tax_rows: list[TaxRow] = []

        for context_block in context_blocks:
            block = context_block.block
            context = context_block.context

            if block.kind == "table":
                for index, row in enumerate(block.rows):
                    row_context = (
                        context_block.row_contexts[index]
                        if index < len(context_block.row_contexts)
                        else context
                    )
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

                    if row_type == ROW_TYPE_TAX and self.section_rules.should_export(row_context.section, text):
                        tax_rows.extend(
                            self.tax_extractor.extract_from_rows(
                                [row],
                                chapter=row_context.chapter,
                                section=row_context.section,
                                group=row_context.group,
                                header=row_context.header,
                            )
                        )
                continue

            row_type, reason = self.row_classifier.classify([block.text])
            semantic_rows.append(
                SemanticRow(
                    row_type="section" if block.text.startswith(f"{context.section} ") or block.text.startswith(f"{context.section} §") else row_type,
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
                    self.tax_extractor.extract_from_rows(
                        [[block.text]],
                        chapter=context.chapter,
                        section=context.section,
                        group=context.group,
                        header=context.header,
                    )
                )

        return SemanticParseResult(semantic_rows=semantic_rows, tax_rows=tax_rows)
