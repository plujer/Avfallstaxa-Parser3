"""Document block with inherited context."""

from __future__ import annotations

from dataclasses import dataclass, field

from parser3.document import DocumentBlock
from parser3.context.context_state import ContextState


@dataclass
class ContextBlock:
    block: DocumentBlock
    context: ContextState
    row_contexts: list[ContextState] = field(default_factory=list)
