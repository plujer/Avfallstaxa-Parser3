"""Single official parser pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from parser3.document import DocumentReader, DocumentBlock
from parser3.models import TaxRow
from parser3.semantic import SemanticParser, SemanticRow
from parser3.trace import TraceStore


@dataclass
class TaxPipelineResult:
    blocks: list[DocumentBlock] = field(default_factory=list)
    semantic_rows: list[SemanticRow] = field(default_factory=list)
    tax_rows: list[TaxRow] = field(default_factory=list)
    trace_store: TraceStore = field(default_factory=TraceStore)


class TaxPipeline:
    def run(self, word_path: str | Path, trace: bool = False) -> TaxPipelineResult:
        blocks = DocumentReader().read(Path(word_path))
        trace_store = TraceStore()
        parsed = SemanticParser(trace_store=trace_store).parse(blocks)
        return TaxPipelineResult(
            blocks=blocks,
            semantic_rows=parsed.semantic_rows,
            tax_rows=parsed.tax_rows,
            trace_store=parsed.trace_store,
        )
