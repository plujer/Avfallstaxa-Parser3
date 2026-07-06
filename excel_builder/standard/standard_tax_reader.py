"""Read EDP standard tax catalog from developer reference workbook."""

from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

from excel_builder.models import StandardTaxCatalog, StandardTaxRow


class StandardTaxReader:
    DEFAULT_PATH = Path("data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")

    FIELD_ALIASES = {
        "strTaxekod": ["strtaxekod", "taxekod", "taxakod"],
        "strTaxebenamning": ["strtaxebenamning", "benämning", "benamning", "taxebenämning", "taxebenamning"],
        "strFaktor": ["strfaktor", "faktor"],
        "strTaxedelAvser": ["strtaxedelavser", "taxedel avser", "taxedel"],
        "strFormel": ["strformel", "formel"],
        "curNuvarandePris": ["curnuvarandepris", "pris", "nuvarande pris"],
    }

    def read(self, path: str | Path | None = None) -> StandardTaxCatalog:
        source = Path(path) if path else self.DEFAULT_PATH
        catalog = StandardTaxCatalog(source_path=str(source))

        if not source.exists():
            catalog.warnings.append(f"Standardtaxefil saknas: {source}")
            return catalog

        wb = load_workbook(source, data_only=True, read_only=False)

        for ws in wb.worksheets:
            header_row = self._find_header_row(ws)
            if header_row is None:
                catalog.warnings.append(f"Kunde inte hitta header i standardtaxeflik: {ws.title}")
                continue

            header_map = self._header_map(ws, header_row)
            if "strTaxekod" not in header_map and "strTaxebenamning" not in header_map:
                catalog.warnings.append(f"Flik saknar taxekod/benämning: {ws.title}")
                continue

            for row_idx in range(header_row + 1, ws.max_row + 1):
                raw: dict[str, str] = {}
                for field, col_idx in header_map.items():
                    raw[field] = self._value(ws.cell(row_idx, col_idx).value)

                if not any(raw.values()):
                    continue

                catalog.rows.append(
                    StandardTaxRow(
                        source_sheet=ws.title,
                        row_number=row_idx,
                        strTaxekod=raw.get("strTaxekod", ""),
                        strTaxebenamning=raw.get("strTaxebenamning", ""),
                        strFaktor=raw.get("strFaktor", ""),
                        strTaxedelAvser=raw.get("strTaxedelAvser", ""),
                        strFormel=raw.get("strFormel", ""),
                        curNuvarandePris=raw.get("curNuvarandePris", ""),
                        raw=raw,
                    )
                )

        return catalog

    def _find_header_row(self, ws) -> int | None:
        for row_idx in range(1, min(ws.max_row, 30) + 1):
            values = [self._norm(ws.cell(row_idx, col_idx).value) for col_idx in range(1, min(ws.max_column, 40) + 1)]
            joined = " | ".join(values)
            if "strtaxekod" in joined or "strtaxebenamning" in joined or "taxekod" in joined:
                return row_idx
        return None

    def _header_map(self, ws, header_row: int) -> dict[str, int]:
        result: dict[str, int] = {}
        for col_idx in range(1, ws.max_column + 1):
            value = self._norm(ws.cell(header_row, col_idx).value)
            if not value:
                continue
            for field, aliases in self.FIELD_ALIASES.items():
                if field in result:
                    continue
                if value in aliases or any(alias in value for alias in aliases):
                    result[field] = col_idx
        return result

    def _norm(self, value) -> str:
        return " ".join(str(value or "").replace("\xa0", " ").lower().strip().split())

    def _value(self, value) -> str:
        if value is None:
            return ""
        return str(value).strip()
