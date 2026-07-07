"""Read Explainable Decision Engine trace CSV files."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import WorkbookDecisionRow


class DecisionTraceCsvReader:
    """Read decision_traces.csv produced by Explainable Decision Engine."""

    def read(self, path: str | Path) -> list[WorkbookDecisionRow]:
        source = Path(path)
        if not source.exists():
            return []

        with source.open("r", newline="", encoding="utf-8-sig") as handle:
            sample = handle.read(4096)
            handle.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=";,\t,") if sample.strip() else csv.excel
            reader = csv.DictReader(handle, dialect=dialect)
            rows: list[WorkbookDecisionRow] = []
            for item in reader:
                rows.append(
                    WorkbookDecisionRow(
                        word_tax_code=str(item.get("word_tax_code", "") or "").strip(),
                        candidate_tax_code=str(item.get("candidate_tax_code", "") or "").strip(),
                        decision=str(item.get("decision", "") or "").strip(),
                        confidence=self._float(item.get("confidence")),
                        total_score=self._float(item.get("total_score")),
                        primary_reason=str(item.get("primary_reason", "") or "").strip(),
                        rejected_reason=str(item.get("rejected_reason", "") or "").strip(),
                        signals=str(item.get("signals", "") or "").strip(),
                    )
                )
            return rows

    def _float(self, value: object) -> float:
        text = str(value or "").strip().replace(",", ".")
        try:
            return float(text)
        except ValueError:
            return 0.0
