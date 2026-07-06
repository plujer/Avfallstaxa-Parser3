from pathlib import Path


def test_knowledge_based_matcher_is_exported():
    text = Path("excel_builder/standard/__init__.py").read_text(encoding="utf-8")
    assert "KnowledgeBasedStandardMatcher" in text


def test_standard_tax_suggestion_engine_uses_knowledge_matcher():
    text = Path("excel_builder/standard/standard_tax_suggestion_engine.py").read_text(encoding="utf-8")
    assert "KnowledgeBasedStandardMatcher" in text
    assert "use_knowledge_matching" in text
