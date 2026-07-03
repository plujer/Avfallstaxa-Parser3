"""Logical page iterator.

Word documents do not always expose reliable page numbers through python-docx.
This class therefore groups blocks into logical pages when explicit page metadata
exists, and otherwise returns one stream. Real rendered-page support can be added
later without changing parser modules.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from parser3.document.document_reader import DocumentBlock


class PageIterator:
    def group_by_page(self, blocks: Iterable[DocumentBlock]) -> dict[int, list[DocumentBlock]]:
        grouped: dict[int, list[DocumentBlock]] = defaultdict(list)
        for block in blocks:
            page = int(block.metadata.get("page", 0) or 0)
            grouped[page].append(block)
        return dict(grouped)
