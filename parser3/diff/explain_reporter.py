from pathlib import Path
from parser3.semantic import SemanticRow

class ExplainReporter:
    def write(self, rows: list[SemanticRow], path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = ["Parser 3.0 explanation report", "", "order | section | group | row_type | reason | text", ""]
        for row in rows:
            lines.append(f"{row.order} | {row.section} | {row.group} | {row.row_type} | {row.reason} | {row.text}")
        out.write_text("\n".join(lines), encoding="utf-8")
        return out
