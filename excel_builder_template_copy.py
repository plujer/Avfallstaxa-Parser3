from __future__ import annotations

import argparse

from excel_builder.template import TemplateMasterManager


def main() -> None:
    parser = argparse.ArgumentParser(description="Create workbook copy from versioned template")
    parser.add_argument("--out", required=True)
    parser.add_argument("--template", default="")
    args = parser.parse_args()

    manager = TemplateMasterManager()
    info = manager.create_working_copy(args.out, args.template or None)

    print("Template copy klar")
    print(f"Template: {info.template_path}")
    print(f"Version: {info.version}")
    print(f"Status: {info.status}")
    print(f"Output: {info.output_path}")
    print(f"Warnings: {len(info.warnings)}")
    for warning in info.warnings:
        print(f"- {warning}")


if __name__ == "__main__":
    main()
