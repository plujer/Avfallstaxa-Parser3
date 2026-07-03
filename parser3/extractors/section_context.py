"""Section context helpers."""

from __future__ import annotations

from dataclasses import dataclass

from parser3.document import DocumentBlock
from parser3.headings import SectionClassifier


@dataclass
class SectionContext:
    section: str = ""
    title: str = ""
    chapter: str = ""
    group: str = ""


class SectionContextBuilder:
    def __init__(self) -> None:
        self.classifier = SectionClassifier()

    def build_for_blocks(self, blocks: list[DocumentBlock]) -> dict[int, SectionContext]:
        contexts: dict[int, SectionContext] = {}
        current = SectionContext()
        chapter = ""

        for block in blocks:
            match = self.classifier.classify(block.text)
            if match:
                if match.level == 1:
                    chapter = match.number
                current = SectionContext(
                    section=match.number,
                    title=match.title,
                    chapter=chapter or match.number.split(".")[0],
                    group="",
                )
            contexts[block.order] = current

        return contexts
