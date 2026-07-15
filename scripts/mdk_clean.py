#!/usr/bin/env python3
"""Clean Keil MDK generated output files."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil

from mdk_common import ensure_project_and_target, output_paths


DEFAULT_RELATIVE_PATHS = [
    "Listings",
    "DebugConfig",
    "build_mdk.log",
    "flash_mdk.log",
]

ALL_PATTERNS = [
    "*.uvoptx",
    "*.uvguix.*",
    "*.uvopt",
    "*.uvgui.*",
]


def safe_resolve(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"refuse to remove outside MDK directory: {resolved}") from exc
    return resolved


def collect_paths(mdk_dir: Path, output_dir: Path, include_all: bool) -> list[Path]:
    matches: list[Path] = []
    seen: set[Path] = set()
    output_dir = safe_resolve(mdk_dir, output_dir)
    if output_dir.exists():
        matches.append(output_dir)
        seen.add(output_dir)

    for relative in DEFAULT_RELATIVE_PATHS:
        path = safe_resolve(mdk_dir, mdk_dir / relative)
        if path.exists() and path not in seen:
            matches.append(path)
            seen.add(path)

    if include_all:
        for pattern in ALL_PATTERNS:
            for path in mdk_dir.glob(pattern):
                resolved = safe_resolve(mdk_dir, path)
                if resolved.exists() and resolved not in seen:
                    matches.append(resolved)
                    seen.add(resolved)

    return sorted(matches, key=lambda item: str(item))


def remove_path(path: Path, dry_run: bool) -> None:
    action = "would remove" if dry_run else "remove"
    print(f"{action}: {path}")
    if dry_run:
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Keil MDK generated files.")
    parser.add_argument("--project", type=Path, help="Path to .uvprojx.")
    parser.add_argument("--target", help="Keil target name.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Also remove Keil user option files such as .uvoptx and .uvguix.*.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path, target_elem, target_name = ensure_project_and_target(
        args.project, args.target, Path.cwd()
    )
    paths = output_paths(project_path, target_elem)
    mdk_dir = project_path.parent

    print(f"project: {project_path}")
    print(f"target: {target_name}")
    print(f"output dir: {paths['dir']}")

    matches = collect_paths(mdk_dir, paths["dir"], args.all)
    if not matches:
        print("clean: nothing to remove")
        return 0
    for path in matches:
        remove_path(path, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
