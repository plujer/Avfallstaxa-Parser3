"""Build a hierarchy of headings from document blocks."""

from __future__ import annotations

from parser3.document.document_reader import DocumentBlock
from parser3.headings.heading import HeadingNode
from parser3.headings.section_classifier import SectionClassifier


class HeadingTreeBuilder:
    """Build heading tree using visible section numbers."""

    def __init__(self, classifier: SectionClassifier | None = None) -> None:
        self.classifier = classifier or SectionClassifier()

    def build(self, blocks: list[DocumentBlock]) -> list[HeadingNode]:
        roots: list[HeadingNode] = []
        stack: list[HeadingNode] = []

        for block in blocks:
            match = self.classifier.classify(block.text)
            if not match:
                continue

            node = HeadingNode(
                number=match.number,
                title=match.title,
                level=match.level,
                order=block.order,
            )

            while stack and stack[-1].level >= node.level:
                stack.pop()

            if stack:
                stack[-1].add_child(node)
            else:
                roots.append(node)

            stack.append(node)

        return roots

    def flatten(self, roots: list[HeadingNode]) -> list[HeadingNode]:
        result: list[HeadingNode] = []

        def walk(node: HeadingNode) -> None:
            result.append(node)
            for child in node.children:
                walk(child)

        for root in roots:
            walk(root)

        return result
