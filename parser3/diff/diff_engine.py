from dataclasses import dataclass, field
from parser3.diff.diff_models import DiffItem
from parser3.models import TaxRow

@dataclass
class DiffResult:
    matched: list[DiffItem] = field(default_factory=list)
    missing: list[DiffItem] = field(default_factory=list)
    extra: list[DiffItem] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.missing and not self.extra

class DiffEngine:
    def compare(self, parsed: list[TaxRow], expected: list[TaxRow]) -> DiffResult:
        parsed_map = self._to_multimap(parsed)
        expected_map = self._to_multimap(expected)
        result = DiffResult()

        for key, expected_rows in expected_map.items():
            parsed_rows = parsed_map.get(key, [])
            match_count = min(len(expected_rows), len(parsed_rows))
            for _ in range(match_count):
                result.matched.append(self._item("matched", key))
            for _ in range(max(0, len(expected_rows) - len(parsed_rows))):
                result.missing.append(self._item("missing", key, "Expected row not found"))

        for key, parsed_rows in parsed_map.items():
            expected_rows = expected_map.get(key, [])
            for _ in range(max(0, len(parsed_rows) - len(expected_rows))):
                result.extra.append(self._item("extra", key, "Extra parser row"))

        return result

    def _to_multimap(self, rows: list[TaxRow]) -> dict[tuple[str, str, str, str], list[TaxRow]]:
        result = {}
        for row in rows:
            if not row.export:
                continue
            key = (self._norm(row.section), self._norm(row.name), self._norm(row.variant), self._norm(row.unit))
            result.setdefault(key, []).append(row)
        return result

    def _item(self, status: str, key: tuple[str, str, str, str], reason: str = "") -> DiffItem:
        return DiffItem(status=status, section=key[0], name=key[1], variant=key[2], unit=key[3], reason=reason)

    def _norm(self, value: str) -> str:
        return " ".join((value or "").replace("\xa0", " ").strip().lower().split())
