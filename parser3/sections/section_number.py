"""Section number utilities."""

from __future__ import annotations


class SectionNumber:
    def __init__(self, value: str) -> None:
        self.value = value

    @property
    def parts(self) -> list[int]:
        return [int(part) for part in self.value.split(".")]

    @property
    def level(self) -> int:
        return len(self.parts)

    @property
    def chapter(self) -> str:
        return str(self.parts[0])

    def is_child_of(self, other: "SectionNumber") -> bool:
        other_parts = other.parts
        return self.parts[: len(other_parts)] == other_parts and self.level > other.level
