def test_context_imports_without_circular_dependency():
    from parser3.context import ContextEngine, SectionContextAssigner
    from parser3.semantic import SemanticParser

    assert ContextEngine is not None
    assert SectionContextAssigner is not None
    assert SemanticParser is not None
