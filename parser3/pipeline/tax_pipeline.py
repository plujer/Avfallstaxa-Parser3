"""Single official parser pipeline.

Architecture rule:
All CLI extraction must go through TaxPipeline. This prevents old extractors from
being used accidentally.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from parser3.document import DocumentReader, DocumentBlock
from parser3.models import TaxRow
from parser3.semantic import SemanticParser, SemanticRow


@dataclass
class TaxPipelineResult:
    blocks: list[DocumentBlock] = field(default_factory=list)
    semantic_rows: list[SemanticRow] = field(default_factory=list)
    tax_rows: list[TaxRow] = field(default_factory=list)


class TaxPipeline:
    def run(self, word_path: str | Path) -> TaxPipelineResult:
        blocks = DocumentReader().read(Path(word_path))
        parsed = SemanticParser().parse(blocks)
        return TaxPipelineResult(
            blocks=blocks,
            semantic_rows=parsed.semantic_rows,
            tax_rows=parsed.tax_rows,
        )
