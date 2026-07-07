from __future__ import annotations

import json
from pathlib import Path

from excel_builder.models.project_metadata_models import ProjectMetadata


class ProjectMetadataReader:
    def read(self, path: str | Path = "version.json") -> ProjectMetadata:
        source = Path(path)
        if not source.exists():
            raise FileNotFoundError(f"Saknar projektmetadata: {source}")
        data = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("version.json måste innehålla ett JSON-objekt")
        return ProjectMetadata.from_dict(data)
