"""Command-line interface for generating Terraform module documentation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tf_doc_gen.generator import TerraformParseError, generate_readme, scan_module


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tf-doc-gen",
        description="Generate README documentation from a Terraform module.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("scan", help="scan a module and update its README")
    scan.add_argument("path", nargs="?", default=".", help="Terraform module directory")
    scan.add_argument(
        "--output",
        default="README.md",
        help="README path, relative to the module directory (default: README.md)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    module_path = Path(args.path).expanduser().resolve()
    if not module_path.is_dir():
        print(f"error: module directory does not exist: {module_path}", file=sys.stderr)
        return 2

    output_path = Path(args.output).expanduser()
    if not output_path.is_absolute():
        output_path = module_path / output_path

    try:
        module = scan_module(module_path)
        generated = generate_readme(module)
        existing = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(merge_generated_section(existing, generated), encoding="utf-8")
    except (OSError, TerraformParseError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Updated {output_path} ({len(module.files)} Terraform files scanned).")
    return 0


def merge_generated_section(existing: str, generated: str) -> str:
    start = "<!-- tf-doc-gen:start -->"
    end = "<!-- tf-doc-gen:end -->"
    managed = f"{start}\n{generated.rstrip()}\n{end}"
    has_start = start in existing
    has_end = end in existing

    if has_start != has_end:
        raise ValueError("README has an incomplete tf-doc-gen marker pair")
    if has_start:
        start_index = existing.index(start)
        end_index = existing.index(end, start_index)
        return f"{existing[:start_index]}{managed}{existing[end_index + len(end):]}"
    if not existing:
        return f"{managed}\n"
    return f"{existing.rstrip()}\n\n{managed}\n"


if __name__ == "__main__":
    raise SystemExit(main())
