from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.models.project_metadata_models import ProjectMetadataReport
from excel_builder.project_metadata import ProjectMetadataReader, ProjectMetadataReporter, ReleaseChecklistBuilder


def main() -> None:
    parser = argparse.ArgumentParser(description="Write Excel Builder project metadata report")
    parser.add_argument("--metadata", default="version.json")
    parser.add_argument("--out", default="output/excel/project_metadata_report.txt")
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    metadata = ProjectMetadataReader().read(metadata_path)
    checklist = ReleaseChecklistBuilder().build(metadata, ".")
    report = ProjectMetadataReport(metadata=metadata, source_path=metadata_path, checklist=checklist)
    out = ProjectMetadataReporter().write(report, args.out)

    print("Projektmetadata verifierad")
    print(f"Version: {metadata.version}")
    print(f"Block: {metadata.block_id} - {metadata.block_name}")
    print(f"Release tag: {metadata.release_tag}")
    print(f"Release ready: {report.is_release_ready}")
    print(f"Rapport: {out}")


if __name__ == "__main__":
    main()
