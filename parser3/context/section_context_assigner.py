"""Assign section context to every document block.

Architecture rule: context layer must not import semantic layer.
"""

from __future__ import annotations

from parser3.context.context_block import ContextBlock
from parser3.context.context_state import ContextState
from parser3.document import DocumentBlock
from parser3.headings import SectionClassifier
from parser3.tables.table_continuation_detector import TableContinuationDetector


class SectionContextAssigner:
    def __init__(self) -> None:
        self.classifier = SectionClassifier()
        self.continuation_detector = TableContinuationDetector()

    def assign(self, blocks: list[DocumentBlock]) -> list[ContextBlock]:
        state = ContextState()
        context_blocks: list[ContextBlock] = []

        for block in blocks:
            match = self.classifier.classify(block.text)
            if match:
                state.section = match.number
                state.chapter = match.number.split(".")[0]
                state.section_title = match.title
                state.group = ""
                state.header = ""
                context_blocks.append(ContextBlock(block=block, context=state.copy()))
                continue

            if block.kind == "paragraph":
                state.group = self._normalize_group(block.text, state.group)

            if block.kind == "table":
                row_contexts: list[ContextState] = []
                for row in block.rows:
                    text = " ".join(c for c in row if c).strip()
                    state.group = self._normalize_group(text, state.group)
                    if self.continuation_detector.is_header_row(row):
                        state.header = text
                    row_contexts.append(state.copy())
                context_blocks.append(ContextBlock(block=block, context=state.copy(), row_contexts=row_contexts))
            else:
                context_blocks.append(ContextBlock(block=block, context=state.copy()))

        return context_blocks

    def _normalize_group(self, text: str, current_group: str = "") -> str:
        lower = (text or "").lower()
        if "tillägg för farligt avfall" in lower:
            return "Tillägg för farligt avfall"
        if "tillägg för el-avfall" in lower:
            return "Tillägg för el-avfall"
        if "övriga avgifter" in lower:
            return "Övriga avgifter"
        return current_group
