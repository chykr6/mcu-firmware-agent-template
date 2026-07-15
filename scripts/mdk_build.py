#!/usr/bin/env python3
"""Build or rebuild a Keil MDK project through UV4.exe."""

from __future__ import annotations

import argparse
from pathlib import Path

from mdk_common import (
    ensure_project_and_target,
    find_uv4,
    output_paths,
    parse_build_result,
    print_log_tail,
    run_uv4,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Keil MDK .uvprojx project.")
    parser.add_argument("--project", type=Path, help="Path to .uvprojx.")
    parser.add_argument("--target", help="Keil target name.")
    parser.add_argument("--uv4", type=Path, help="Path to UV4.exe.")
    parser.add_argument("--rebuild", action="store_true", help="Run a full rebuild.")
    parser.add_argument("--log", type=Path, help="Build log path.")
    parser.add_argument("--tail", type=int, default=80, help="Lines of log tail to print.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path, target_elem, target_name = ensure_project_and_target(
        args.project, args.target, Path.cwd()
    )
    paths = output_paths(project_path, target_elem)
    log_path = args.log.resolve() if args.log else paths["build_log"]
    uv4 = find_uv4(args.uv4)
    action = "-r" if args.rebuild else "-b"

    print(f"project: {project_path}")
    print(f"target: {target_name}")
    print(f"uv4: {uv4}")
    print(f"log: {log_path}")

    rc = run_uv4(uv4, action, project_path, target_name, log_path)
    errors, warnings = parse_build_result(log_path)
    if errors is not None:
        print(f"result: {errors} Error(s), {warnings} Warning(s)")
    else:
        print("result: build summary not found")

    if rc != 0:
        print_log_tail(log_path, args.tail)
        return rc
    if errors is not None and errors > 0:
        print_log_tail(log_path, args.tail)
        return 1

    print_log_tail(log_path, args.tail)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
