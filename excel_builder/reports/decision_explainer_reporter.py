"""Write Explainable Decision Engine reports."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import ExplainableDecisionReport


class DecisionExplainerReporter:
    def write(self, report: ExplainableDecisionReport, out_dir: str | Path = "output/excel") -> None:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        self.write_text(report, out_path / "explainable_decision_report.txt")
        self.write_csv(report, out_path / "decision_traces.csv")

    def write_text(self, report: ExplainableDecisionReport, path: str | Path) -> None:
        counts = Counter(trace.decision for trace in report.traces)
        lines = [
            "Explainable Decision Engine Report",
            "",
            "Status: Förklarar beslut från Composite Matching Engine med confidence och spårbara signaler.",
            "Taxa_från_edp ändras inte. Standardtaxor är endast beslutsstöd.",
            f"Traces: {report.total_traces}",
            f"ACCEPT: {counts.get('ACCEPT', 0)}",
            f"REVIEW: {counts.get('REVIEW', 0)}",
            f"REJECT: {counts.get('REJECT', 0)}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Top decision traces:",
        ]
        for trace in sorted(report.traces, key=lambda item: item.confidence, reverse=True)[:25]:
            lines.append(
                f"- {trace.decision} confidence={trace.confidence:.4f} score={trace.total_score:.4f} | "
                f"{trace.word_tax_code} -> {trace.candidate_tax_code} | {trace.primary_reason}"
            )
        if report.warnings:
            lines += ["", "Warnings:"] + [f"- {warning}" for warning in report.warnings[:50]]
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_csv(self, report: ExplainableDecisionReport, path: str | Path) -> None:
        fieldnames = [
            "word_tax_code",
            "candidate_tax_code",
            "decision",
            "confidence",
            "total_score",
            "primary_reason",
            "rejected_reason",
            "signals",
        ]
        with Path(path).open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for trace in sorted(report.traces, key=lambda item: (item.decision, -item.confidence)):
                signals = " | ".join(
                    f"{part.signal}:{part.score:.2f}*{part.weight:.2f}={part.contribution:.4f}"
                    for part in trace.parts
                )
                writer.writerow(
                    {
                        "word_tax_code": trace.word_tax_code,
                        "candidate_tax_code": trace.candidate_tax_code,
                        "decision": trace.decision,
                        "confidence": f"{trace.confidence:.4f}",
                        "total_score": f"{trace.total_score:.4f}",
                        "primary_reason": trace.primary_reason,
                        "rejected_reason": trace.rejected_reason,
                        "signals": signals,
                    }
                )
