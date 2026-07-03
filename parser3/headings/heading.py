"""Heading domain objects."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class HeadingMatch:
    number: str
    title: str
    level: int
    raw_text: str


@dataclass
class HeadingNode:
    number: str
    title: str
    level: int
    order: int = 0
    children: list["HeadingNode"] = field(default_factory=list)

    def add_child(self, node: "HeadingNode") -> None:
        self.children.append(node)

    @property
    def full_title(self) -> str:
        return f"{self.number} {self.title}".strip()
