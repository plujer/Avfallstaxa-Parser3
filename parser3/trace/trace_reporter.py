"""Write trace report."""

from __future__ import annotations

from pathlib import Path

from parser3.trace.trace_models import TraceStore


class TraceReporter:
    def write(self, store: TraceStore, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Parser Extractor Trace Report",
            "",
            f"Events: {len(store.events)}",
            "",
        ]

        for event in store.events:
            lines.append("=" * 100)
            lines.append(f"component: {event.component}")
            lines.append(f"section: {event.section}")
            if event.order is not None:
                lines.append(f"order: {event.order}")
            lines.append(f"decision: {event.decision}")
            lines.append(f"reason: {event.reason}")
            lines.append(f"score: {event.score:.3f}")
            lines.append(f"best_match: {event.best_match}")
            lines.append(f"input_text: {event.input_text}")
            lines.append(f"normalized_text: {event.normalized_text}")
            lines.append("")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
