from dataclasses import dataclass, field
from parser3.document import DocumentBlock
from parser3.extractors import TaxRowExtractor
from parser3.headings import SectionClassifier
from parser3.models import TaxRow
from parser3.semantic.row_type_classifier import RowTypeClassifier
from parser3.semantic.section_tax_rules import SectionTaxRules
from parser3.semantic.semantic_context import SemanticContext
from parser3.semantic.semantic_row import SemanticRow
from parser3.tables import SmartTableDetector
from parser3.utils.constants import ROW_TYPE_GROUP, ROW_TYPE_HEADER, ROW_TYPE_REFERENCE, ROW_TYPE_TAX

@dataclass
class SemanticParseResult:
    semantic_rows: list[SemanticRow] = field(default_factory=list)
    tax_rows: list[TaxRow] = field(default_factory=list)

class SemanticParser:
    def __init__(self) -> None:
        self.section_classifier = SectionClassifier()
        self.row_classifier = RowTypeClassifier()
        self.section_rules = SectionTaxRules()
        self.table_detector = SmartTableDetector()
        self.tax_extractor = TaxRowExtractor()

    def parse(self, blocks: list[DocumentBlock]) -> SemanticParseResult:
        context = SemanticContext()
        semantic_rows: list[SemanticRow] = []
        tax_rows: list[TaxRow] = []
        tables_by_order = {t.start_order: t for t in self.table_detector.detect(blocks)}

        for block in blocks:
            match = self.section_classifier.classify(block.text)
            if match:
                context.section = match.number
                context.chapter = match.number.split(".")[0]
                context.section_title = match.title
                context.group = ""
                context.header = ""
                semantic_rows.append(SemanticRow("section", block.text, [block.text], block.order, context.section, context.group, "section heading"))
                continue

            if block.order in tables_by_order:
                table = tables_by_order[block.order]
                for row in table.rows:
                    row_type, reason = self.row_classifier.classify(row)
                    text = " ".join(c for c in row if c).strip()
                    if row_type == ROW_TYPE_GROUP:
                        context.group = self.section_rules.normalize_group(text, context.group)
                    elif row_type == ROW_TYPE_HEADER:
                        context.header = text
                    semantic_rows.append(SemanticRow(row_type, text, row, block.order, context.section, context.group, reason))
                    if row_type == ROW_TYPE_TAX and self.section_rules.should_export(context.section, text):
                        tax_rows.extend(self.tax_extractor.extract_from_rows([row], chapter=context.chapter, section=context.section, group=context.group, header=context.header))
                continue

            row_type, reason = self.row_classifier.classify([block.text])
            if row_type == ROW_TYPE_GROUP:
                context.group = self.section_rules.normalize_group(block.text, context.group)
            semantic_rows.append(SemanticRow(row_type, block.text, [block.text], block.order, context.section, context.group, reason))
            if row_type == ROW_TYPE_TAX and self.section_rules.should_export(context.section, block.text):
                tax_rows.extend(self.tax_extractor.extract_from_rows([[block.text]], chapter=context.chapter, section=context.section, group=context.group, header=context.header))

        return SemanticParseResult(semantic_rows=semantic_rows, tax_rows=tax_rows)
