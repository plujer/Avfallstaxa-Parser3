from openpyxl import Workbook
from excel_builder.io import WorkbookSnapshot


def test_workbook_snapshot_writes_selected_sheets(tmp_path):
    path = tmp_path / "arbets.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Taxepunkter"
    ws.append(["Paragraf", "Taxapunkt"])
    ws.append(["6.1.2", "Asbest"])
    wb.create_sheet("Taxa_från_edp")
    wb.save(path)

    out = WorkbookSnapshot().write_snapshot(path, tmp_path / "snapshot.txt", max_rows=5)
    text = out.read_text(encoding="utf-8")

    assert "Sheet: Taxepunkter" in text
    assert "Asbest" in text
    assert "Sheet: Taxa_från_edp" in text
