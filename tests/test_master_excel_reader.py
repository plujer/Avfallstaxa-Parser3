from openpyxl import Workbook
from parser3.excel import MasterExcelReader

def test_master_excel_reader_reads_basic_rows(tmp_path):
    path = tmp_path / "master.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Paragraf", "Taxepunkt", "Variant", "Enhet"])
    ws.append(["6.1.2", "Asbest", "", "kilogram"])
    wb.save(path)
    rows = MasterExcelReader().read(path)
    assert len(rows) == 1
    assert rows[0].section == "6.1.2"
    assert rows[0].name == "Asbest"
    assert rows[0].unit == "kilogram"
