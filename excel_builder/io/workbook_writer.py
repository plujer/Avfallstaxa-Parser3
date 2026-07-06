"""Write a new Arbets-Excel from parser rows."""

from __future__ import annotations

from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo

from excel_builder.models import BuilderResult


class WorkbookWriter:
    HEADERS = [
        "Paragraf",
        "Paragrafnamn",
        "Taxapunkt",
        "Variant",
        "Enhet",
        "Pris från Word",
        "EDP taxekod",
        "EDP koppling status",
        "Kommentar",
        "Källa",
    ]

    def write(self, result: BuilderResult, path: str | Path = "output/excel/ArbetsExcel_byggd_fran_parser.xlsx") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.title = "Taxepunkter"

        ws.append(self.HEADERS)

        for row in result.rows:
            ws.append([
                row.section,
                "",
                row.name,
                row.variant,
                row.unit,
                row.price,
                "",
                "Ej kopplad",
                "",
                row.source,
            ])

        self._style(ws)
        self._add_table(ws)
        self._add_summary_sheet(wb, result)
        self._add_readme_sheet(wb)

        wb.save(out)
        return out

    def _style(self, ws) -> None:
        header_fill = PatternFill("solid", fgColor="D9EAF7")
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = header_fill
            cell.alignment = Alignment(wrap_text=True)

        widths = {
            "A": 14,
            "B": 28,
            "C": 55,
            "D": 32,
            "E": 16,
            "F": 18,
            "G": 18,
            "H": 22,
            "I": 35,
            "J": 24,
        }
        for col, width in widths.items():
            ws.column_dimensions[col].width = width

        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    def _add_table(self, ws) -> None:
        if ws.max_row < 2:
            return
        ref = f"A1:J{ws.max_row}"
        table = Table(displayName="TaxepunkterTable", ref=ref)
        style = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        table.tableStyleInfo = style
        ws.add_table(table)

    def _add_summary_sheet(self, wb, result: BuilderResult) -> None:
        ws = wb.create_sheet("Sammanfattning")
        ws.append(["Mått", "Värde"])
        ws.append(["Antal rader från parser", result.row_count])
        ws.append(["Varningar", len(result.warnings)])
        ws.append(["Status", "Arbets-Excel – inte master"])
        ws.column_dimensions["A"].width = 35
        ws.column_dimensions["B"].width = 45
        for cell in ws[1]:
            cell.font = Font(bold=True)

    def _add_readme_sheet(self, wb) -> None:
        ws = wb.create_sheet("README")
        rows = [
            ["Excel Builder v2.0.0-alpha.1"],
            [""],
            ["Denna fil är en arbets-Excel."],
            ["Den är inte master förrän användaren uttryckligen godkänner den."],
            [""],
            ["Nästa steg:"],
            ["1. Koppla mot befintlig Arbets-Excel/EDP-data."],
            ["2. Behåll befintliga EDP-koder där matchning är säker."],
            ["3. Markera osäkra rader för manuell kontroll."],
            ["4. Skapa ny godkänd arbetsversion."],
        ]
        for row in rows:
            ws.append(row)
        ws.column_dimensions["A"].width = 90
