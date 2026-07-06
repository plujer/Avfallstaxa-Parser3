from parser3.extractors import Section612Extractor
from parser3.trace import TraceStore


def test_section612_trace_records_export_decision():
    store = TraceStore()
    extractor = Section612Extractor(trace_store=store)
    rows = extractor.extract_line("Betong, lättbetong kilogram", chapter="6", section="6.1.2", order=123)

    assert len(rows) == 1
    assert store.events
    event = store.events[-1]
    assert event.component == "Section612Extractor"
    assert event.decision == "exported"
    assert event.order == 123


def test_section612_trace_records_not_exported_decision():
    store = TraceStore()
    extractor = Section612Extractor(trace_store=store)
    rows = extractor.extract_line("Detta är vanlig information", chapter="6", section="6.1.2", order=123)

    assert rows == []
    assert store.events
    assert store.events[-1].decision == "not_exported"
