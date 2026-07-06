"""Manage versioned master workbook templates.

Rules:
- A generated workbook must start as a copy of the template.
- The template/master must never be overwritten automatically.
- Any change to the template structure requires user approval and a new versioned template file.
"""

from __future__ import annotations

from pathlib import Path
import re
import shutil

from excel_builder.models import TemplateInfo


class TemplateMasterManager:
    DEFAULT_TEMPLATE_DIR = Path("data/master_templates")
    DEFAULT_TEMPLATE_NAME = "ArbetsExcel_Template_v0.1.0_draft.xlsx"

    def get_default_template(self) -> TemplateInfo:
        path = self.DEFAULT_TEMPLATE_DIR / self.DEFAULT_TEMPLATE_NAME
        version = self._extract_version(path.name)
        status = "draft"
        if "locked" in path.stem.lower():
            status = "locked"

        info = TemplateInfo(template_path=str(path), version=version, status=status)
        if not path.exists():
            info.warnings.append(f"Template saknas: {path}")
        return info

    def create_working_copy(self, output_path: str | Path, template_path: str | Path | None = None) -> TemplateInfo:
        source = Path(template_path) if template_path else Path(self.get_default_template().template_path)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        info = TemplateInfo(
            template_path=str(source),
            version=self._extract_version(source.name),
            status="locked" if "locked" in source.stem.lower() else "draft",
            output_path=str(output),
        )

        if not source.exists():
            info.warnings.append(f"Template saknas: {source}")
            return info

        if source.resolve() == output.resolve():
            info.warnings.append("Output får inte vara samma fil som template/master.")
            return info

        shutil.copy2(source, output)
        return info

    def propose_new_template_name(self, version: str, status: str = "draft") -> str:
        safe_version = version if version.startswith("v") else f"v{version}"
        safe_status = re.sub(r"[^A-Za-z0-9_-]+", "_", status.strip().lower() or "draft")
        return f"ArbetsExcel_Template_{safe_version}_{safe_status}.xlsx"

    def _extract_version(self, filename: str) -> str:
        match = re.search(r"v(\d+\.\d+\.\d+)", filename)
        if match:
            return f"v{match.group(1)}"
        match = re.search(r"v(\d+\.\d+)", filename)
        if match:
            return f"v{match.group(1)}"
        return "unknown"
