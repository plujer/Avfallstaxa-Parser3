"""Write Composite Matching Engine reports."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import CompositeMatchingReport


class CompositeMatchingReporter:
    def write(self, report: CompositeMatchingReport, out_dir: str | Path = "output/excel") -> None:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        self.write_text(report, out_path / "composite_matching_report.txt")
        self.write_csv(report, out_path / "composite_matches.csv")

    def write_text(self, report: CompositeMatchingReport, path: str | Path) -> None:
        status_counts = Counter(result.status for result in report.results)
        lines = [
            "Composite Matching Engine Report",
            "",
            "Status: Vägt beslutsstöd från struktur, kontext, taxefamilj, variant, attribut, EDP och standardtaxa.",
            "Taxa_från_edp ändras inte. Kommununik data delas inte mellan kommunprojekt.",
            f"Results: {report.total_results}",
            f"MATCH: {status_counts.get('MATCH', 0)}",
            f"REVIEW: {status_counts.get('REVIEW', 0)}",
            f"NO_MATCH: {status_counts.get('NO_MATCH', 0)}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Top composite results:",
        ]
        for result in sorted(report.results, key=lambda item: item.score, reverse=True)[:25]:
            lines.append(f"- {result.status} {result.score:.4f} | {result.word_tax_code} -> {result.candidate_tax_code} | {result.explanation}")
        if report.warnings:
            lines += ["", "Warnings:"] + [f"- {warning}" for warning in report.warnings[:50]]
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_csv(self, report: CompositeMatchingReport, path: str | Path) -> None:
        fieldnames = [
            "word_tax_code",
            "candidate_tax_code",
            "status",
            "score",
            "explanation",
            "edp_exact",
            "tax_family",
            "variant",
            "semantic_attributes",
            "hierarchical_context",
            "document_structure",
        ]
        with Path(path).open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for result in sorted(report.results, key=lambda item: (item.status, -item.score, item.word_tax_code)):
                part_scores = {part.name: part.score for part in result.parts}
                writer.writerow(
                    {
                        "word_tax_code": result.word_tax_code,
                        "candidate_tax_code": result.candidate_tax_code,
                        "status": result.status,
                        "score": f"{result.score:.4f}",
                        "explanation": result.explanation,
                        "edp_exact": part_scores.get("edp_exact", 0.0),
                        "tax_family": part_scores.get("tax_family", 0.0),
                        "variant": part_scores.get("variant", 0.0),
                        "semantic_attributes": part_scores.get("semantic_attributes", 0.0),
                        "hierarchical_context": part_scores.get("hierarchical_context", 0.0),
                        "document_structure": part_scores.get("document_structure", 0.0),
                    }
                )
