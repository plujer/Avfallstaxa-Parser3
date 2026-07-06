"""Pipeline architecture reporter."""

from __future__ import annotations

from pathlib import Path

from parser3.pipeline.tax_pipeline import TaxPipelineResult


class PipelineReporter:
    def write(self, result: TaxPipelineResult, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        block_counts: dict[str, int] = {}
        for block in result.blocks:
            block_counts[block.kind] = block_counts.get(block.kind, 0) + 1

        lines = [
            "Parser 3.1 architecture report",
            "",
            "Official pipeline:",
            "DocumentReader -> ContextEngine -> SemanticParser -> Unified extractors -> Export",
            "",
            f"Blocks: {len(result.blocks)}",
            f"Semantic rows: {len(result.semantic_rows)}",
            f"Tax rows: {len(result.tax_rows)}",
            "",
            "Block types:",
        ]

        for kind, count in sorted(block_counts.items()):
            lines.append(f"- {kind}: {count}")

        out.write_text("\\n".join(lines), encoding="utf-8")
        return out
