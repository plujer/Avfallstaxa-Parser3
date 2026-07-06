"""Build a lightweight document tree from headings and blocks."""

from __future__ import annotations

from dataclasses import dataclass, field

from parser3.document import DocumentBlock
from parser3.headings import SectionClassifier


@dataclass
class DocumentNode:
    section: str
    title: str
    level: int
    start_order: int
    blocks: list[DocumentBlock] = field(default_factory=list)
    children: list["DocumentNode"] = field(default_factory=list)


class DocumentTreeBuilder:
    def __init__(self) -> None:
        self.classifier = SectionClassifier()

    def build(self, blocks: list[DocumentBlock]) -> list[DocumentNode]:
        roots: list[DocumentNode] = []
        stack: list[DocumentNode] = []
        current: DocumentNode | None = None

        for block in blocks:
            match = self.classifier.classify(block.text)
            if match:
                node = DocumentNode(
                    section=match.number,
                    title=match.title,
                    level=match.level,
                    start_order=block.order,
                    blocks=[block],
                )

                while stack and stack[-1].level >= node.level:
                    stack.pop()

                if stack:
                    stack[-1].children.append(node)
                else:
                    roots.append(node)

                stack.append(node)
                current = node
                continue

            if current is not None:
                current.blocks.append(block)

        return roots

    def flatten(self, nodes: list[DocumentNode]) -> list[DocumentNode]:
        result: list[DocumentNode] = []

        def walk(node: DocumentNode) -> None:
            result.append(node)
            for child in node.children:
                walk(child)

        for node in nodes:
            walk(node)

        return result
