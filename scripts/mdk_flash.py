#!/usr/bin/env python3
"""Download a Keil MDK project to target through UV4.exe."""

from __future__ import annotations

import argparse
from pathlib import Path

from mdk_common import (
    ensure_project_and_target,
    find_uv4,
    output_paths,
    print_log_tail,
    run_uv4,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Flash a Keil MDK .uvprojx target.")
    parser.add_argument("--project", type=Path, help="Path to .uvprojx.")
    parser.add_argument("--target", help="Keil target name.")
    parser.add_argument("--uv4", type=Path, help="Path to UV4.exe.")
    parser.add_argument("--log", type=Path, help="Flash log path.")
    parser.add_argument("--tail", type=int, default=60, help="Lines of log tail to print.")
    parser.add_argument(
        "--require-hex",
        action="store_true",
        help="Fail before flashing if the expected HEX file does not exist.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path, target_elem, target_name = ensure_project_and_target(
        args.project, args.target, Path.cwd()
    )
    paths = output_paths(project_path, target_elem)
    log_path = args.log.resolve() if args.log else paths["flash_log"]
    uv4 = find_uv4(args.uv4)

    if args.require_hex and not paths["hex"].exists():
        print(f"HEX not found: {paths['hex']}")
        print("Run: python scripts/mdk_build.py --rebuild")
        return 2

    print(f"project: {project_path}")
    print(f"target: {target_name}")
    print(f"uv4: {uv4}")
    print(f"expected hex: {paths['hex']}")
    print(f"log: {log_path}")

    rc = run_uv4(uv4, "-f", project_path, target_name, log_path)
    print_log_tail(log_path, args.tail)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
