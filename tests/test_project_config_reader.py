import json

from excel_builder.project import ProjectConfigReader


def test_project_config_reader_reads_config(tmp_path):
    path = tmp_path / "project_config.json"
    path.write_text(json.dumps({
        "municipality": "Sorsele",
        "word_path": "data/projects/Sorsele/taxadokument.docx",
        "edp_export_path": "data/edp_exports/Sorsele.xlsx",
        "output_dir": "output/projects/Sorsele",
        "parser_result_path": "output/reports/parser3_result.json",
        "notes": "test",
    }, ensure_ascii=False), encoding="utf-8")

    config = ProjectConfigReader().read(path)

    assert config.municipality == "Sorsele"
    assert config.edp_export_path.endswith("Sorsele.xlsx")
    assert config.output_dir.endswith("Sorsele")
