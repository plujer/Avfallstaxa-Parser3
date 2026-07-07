"""Reports for semantic candidate ranking."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from excel_builder.models import SemanticCandidateReport


class SemanticCandidateReporter:
    HEADERS = [
        "Word source ID",
        "Candidate source",
        "Candidate source ID",
        "Score",
        "Status",
        "Candidate tax code",
        "Candidate standard tax code",
        "Word category",
        "Candidate category",
        "Word waste type",
        "Candidate waste type",
        "Word service type",
        "Candidate service type",
        "Word container type",
        "Candidate container type",
        "Word volume",
        "Candidate volume",
        "Word factor",
        "Candidate factor",
        "Explanation",
        "Word text",
        "Candidate text",
    ]

    def write_txt(self, report: SemanticCandidateReport, path: str | Path = "output/excel/semantic_candidate_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        statuses = Counter(candidate.status for candidate in report.candidates)
        sources = Counter(candidate.candidate_profile.source for candidate in report.candidates)

        lines = [
            "Semantic Candidate Ranking Report",
            "",
            "Status: Poängbaserad ranking mellan Word-profiler och kandidater från standardtaxor/regler.",
            "Detta ändrar inte Taxa_från_edp.",
            f"Total candidates: {report.total_candidates}",
            f"Word profiles with candidates: {report.unique_word_profiles}",
            "",
            "Statuses:",
        ]

        for status, count in sorted(statuses.items()):
            lines.append(f"- {status}: {count}")

        lines.append("")
        lines.append("Candidate sources:")
        for source, count in sorted(sources.items()):
            lines.append(f"- {source}: {count}")

        lines.append("")
        lines.append("Top candidates:")
        for candidate in sorted(report.candidates, key=lambda item: item.score, reverse=True)[:50]:
            lines.append(
                f"- {candidate.word_profile.source_id} -> {candidate.candidate_profile.source} "
                f"{candidate.candidate_profile.tax_code or candidate.candidate_profile.standard_tax_code} "
                f"score={candidate.score:.2f} status={candidate.status} | {candidate.explanation}"
            )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: SemanticCandidateReport, path: str | Path = "output/excel/semantic_candidates.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for candidate in report.candidates:
                word_key = candidate.word_profile.key
                cand_key = candidate.candidate_profile.key
                writer.writerow([
                    candidate.word_profile.source_id,
                    candidate.candidate_profile.source,
                    candidate.candidate_profile.source_id,
                    f"{candidate.score:.4f}",
                    candidate.status,
                    candidate.candidate_profile.tax_code,
                    candidate.candidate_profile.standard_tax_code,
                    word_key.category,
                    cand_key.category,
                    word_key.waste_type,
                    cand_key.waste_type,
                    word_key.service_type,
                    cand_key.service_type,
                    word_key.container_type,
                    cand_key.container_type,
                    word_key.container_volume_liter,
                    cand_key.container_volume_liter,
                    word_key.factor_hint,
                    cand_key.factor_hint,
                    candidate.explanation,
                    candidate.word_profile.source_text,
                    candidate.candidate_profile.source_text,
                ])

        return out
