from __future__ import annotations

import argparse

from excel_builder.project import ProjectConfigReader, ProjectRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run isolated Excel Builder project")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = ProjectConfigReader().read(args.config)
    result = ProjectRunner().run(config)

    print("Isolerad projektkörning klar")
    print(f"Kommun: {result.config.municipality}")
    print(f"Excel: {result.excel_path}")
    print(f"Rapport: {result.report_path}")
    print(f"Manifest: {result.manifest_path}")
    print(f"Warnings: {len(result.warnings)}")


if __name__ == "__main__":
    main()
