from pathlib import Path


def test_dynamic_taxepunkter_reader_is_exported():
    text = Path("excel_builder/rules/__init__.py").read_text(encoding="utf-8")
    assert "DynamicTaxepunkterReader" in text


def test_master_repository_imports_dynamic_reader():
    text = Path("excel_builder/rules/master_rule_repository_reader.py").read_text(encoding="utf-8")
    assert "DynamicTaxepunkterReader" in text
    assert "dynamic_taxepunkter_reader.read" in text
