import json
from excel_builder.io import ParserResultReader


def test_parser_result_reader_reads_rows(tmp_path):
    path = tmp_path / "parser3_result.json"
    path.write_text(json.dumps([
        {"section": "6.1.2", "name": "Asbest, emballerat", "unit": "kilogram", "price": "", "export": True},
        {"section": "6.1.2", "name": "Info", "export": False},
    ]), encoding="utf-8")

    result = ParserResultReader().read(path)

    assert result.row_count == 1
    assert result.rows[0].name == "Asbest, emballerat"
