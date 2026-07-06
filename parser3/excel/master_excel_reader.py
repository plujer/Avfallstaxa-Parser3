from pathlib import Path
from openpyxl import load_workbook
from parser3.models import TaxRow

class MasterExcelReader:
    SECTION_NAMES = {"section", "paragraf", "§", "kapitel"}
    NAME_NAMES = {"name", "taxepunkt", "taxa", "benämning", "tjänst", "typ av avfall"}
    VARIANT_NAMES = {"variant", "intervall", "avgiftstyp"}
    UNIT_NAMES = {"unit", "enhet"}

    def read(self, path: str | Path, sheet_name: str | None = None) -> list[TaxRow]:
        wb = load_workbook(Path(path), data_only=True)
        ws = wb[sheet_name] if sheet_name else wb[wb.sheetnames[0]]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return []
        header_index = self._find_header_index(rows)
        if header_index is None:
            return []
        headers = [self._norm_header(v) for v in rows[header_index]]
        col = self._column_map(headers)
        result = []
        for row in rows[header_index + 1:]:
            section = self._cell(row, col.get("section"))
            name = self._cell(row, col.get("name"))
            variant = self._cell(row, col.get("variant"))
            unit = self._cell(row, col.get("unit"))
            if name:
                result.append(TaxRow(section=section, name=name, variant=variant, unit=unit, export=True))
        return result

    def _find_header_index(self, rows: list[tuple]) -> int | None:
        for idx, row in enumerate(rows[:30]):
            headers = {self._norm_header(v) for v in row}
            if headers & self.NAME_NAMES:
                return idx
        return None

    def _column_map(self, headers: list[str]) -> dict[str, int]:
        result = {}
        for idx, header in enumerate(headers):
            if header in self.SECTION_NAMES:
                result["section"] = idx
            elif header in self.NAME_NAMES:
                result["name"] = idx
            elif header in self.VARIANT_NAMES:
                result["variant"] = idx
            elif header in self.UNIT_NAMES:
                result["unit"] = idx
        return result

    def _cell(self, row: tuple, index: int | None) -> str:
        if index is None or index >= len(row):
            return ""
        value = row[index]
        return "" if value is None else str(value).strip()

    def _norm_header(self, value) -> str:
        return " ".join(str(value or "").strip().lower().split())
