from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

from excel_builder.io import WorkbookProfiler
from excel_builder.reports import WorkbookProfileReporter


def test_workbook_profiler_detects_headers_tables_hidden_columns_and_validations(tmp_path):
    path = tmp_path / "arbets.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Taxepunkter"
    ws.append(["Paragraf", "Taxapunkt", "Variant", "Enhet", "Föreslagen taxa", "Taxakod"])
    ws.append(["6.1.2", "Asbest, emballerat", "", "kilogram", "22,88", "KOD1"])

    table = Table(displayName="TaxepunkterTable", ref="A1:F2")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(table)

    ws.column_dimensions["F"].hidden = True
    ws.freeze_panes = "A2"
    ws["G2"] = "=E2"

    wb.save(path)

    profile = WorkbookProfiler().profile(path)

    assert profile.sheet_count == 1
    sheet = profile.sheets[0]
    assert sheet.name == "Taxepunkter"
    assert sheet.likely_header_row == 1
    assert sheet.detected_fields["section"] == "A"
    assert sheet.detected_fields["tax_point"] == "B"
    assert sheet.detected_fields["unit"] == "D"
    assert sheet.detected_fields["price"] == "E"
    assert sheet.detected_fields["edp_code"] == "F"
    assert sheet.tables[0].name == "TaxepunkterTable"
    assert next(col for col in sheet.columns if col.letter == "F").hidden


def test_workbook_profile_reporter_writes_report(tmp_path):
    path = tmp_path / "missing.xlsx"
    profile = WorkbookProfiler().profile(path)
    report = WorkbookProfileReporter().write(profile, tmp_path / "report.txt")

    text = report.read_text(encoding="utf-8")
    assert "Arbets-Excel Profile Report" in text
    assert "Arbets-Excel saknas" in text
