#!/usr/bin/env python3
"""Shared helpers for Keil MDK command-line scripts."""

from __future__ import annotations

import json
import os
import locale
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET


IGNORED_SEARCH_DIRS = {
    ".git",
    ".vscode",
    ".cache",
    "__pycache__",
    "Objects",
    "Listings",
    "DebugConfig",
    "node_modules",
    "dist",
    "build",
}
COMMON_PROJECT_DIRS = {"mdk-arm", "mdk", "keil"}
REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLCHAIN_LOCAL = REPO_ROOT / "toolchain.local.json"
WINDOW_HIDE = 0


def load_toolchain(config_path: Path | None = None) -> dict:
    path = config_path or TOOLCHAIN_LOCAL
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    if not path.exists():
        raise SystemExit(f"toolchain config not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid toolchain json: {path}: {exc}") from exc


def elem_text(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return "".join(elem.itertext()).strip()


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def find_project_file(search_root: Path) -> Path:
    search_root = search_root.resolve()
    candidates: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(search_root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_SEARCH_DIRS]
        for filename in filenames:
            if filename.lower().endswith(".uvprojx"):
                candidates.append((Path(dirpath) / filename).resolve())

    if not candidates:
        raise SystemExit(f"No .uvprojx file found under {search_root}")
    if len(candidates) == 1:
        return candidates[0]

    common_dir_matches = [
        path for path in candidates if path.parent.name.lower() in COMMON_PROJECT_DIRS
    ]
    if len(common_dir_matches) == 1:
        return common_dir_matches[0]

    relative = [str(path.relative_to(search_root)) for path in candidates]
    raise SystemExit(
        "Multiple .uvprojx files found. Please specify --project. "
        f"Candidates: {', '.join(relative)}"
    )


def load_project(project_path: Path) -> ET.Element:
    return ET.parse(project_path).getroot()


def target_name(target: ET.Element) -> str:
    return elem_text(target.find("TargetName"))


def find_target(root: ET.Element, requested: str | None, project_path: Path) -> ET.Element:
    targets = root.findall(".//Target")
    if not targets:
        raise SystemExit(f"No targets found in {project_path}")

    if requested:
        for target in targets:
            if target_name(target) == requested:
                return target

        available = [target_name(target) for target in targets]
        raise SystemExit(
            f"Target '{requested}' not found. Available targets: {', '.join(available)}"
        )

    if len(targets) == 1:
        return targets[0]

    project_stem = normalize_name(project_path.stem)
    for target in targets:
        if normalize_name(target_name(target)) == project_stem:
            return target

    available = [target_name(target) for target in targets]
    raise SystemExit(
        "Multiple targets found. Please specify --target. "
        f"Available targets: {', '.join(available)}"
    )


def target_common_option(target: ET.Element) -> ET.Element:
    common = target.find("./TargetOption/TargetCommonOption")
    if common is None:
        raise SystemExit(f"Target '{target_name(target)}' has no TargetCommonOption")
    return common


def resolve_mdk_path(project_dir: Path, value: str) -> Path:
    value = value.strip().strip('"').replace("\\", os.sep)
    path = Path(value)
    if not path.is_absolute():
        path = project_dir / path
    return path.resolve()


def output_paths(project_path: Path, target: ET.Element) -> dict[str, Path]:
    common = target_common_option(target)
    out_dir = elem_text(common.find("OutputDirectory")) or ".\\Objects\\"
    out_name = elem_text(common.find("OutputName")) or "output"
    resolved_out_dir = resolve_mdk_path(project_path.parent, out_dir)
    return {
        "dir": resolved_out_dir,
        "axf": resolved_out_dir / f"{out_name}.axf",
        "hex": resolved_out_dir / f"{out_name}.hex",
        "build_log": project_path.parent / "build_mdk.log",
        "flash_log": project_path.parent / "flash_mdk.log",
    }


def find_uv4(explicit: Path | None = None) -> Path:
    if explicit is not None:
        uv4 = explicit.resolve()
        if uv4.exists():
            return uv4
        raise SystemExit(f"uVision executable not found: {uv4}")

    config = load_toolchain()
    uv4_dir = str(config.get("mdk", {}).get("uv4_dir", "")).strip()
    if not uv4_dir:
        raise SystemExit("toolchain.local.json missing mdk.uv4_dir")

    uv4_dir_path = Path(uv4_dir)
    if not uv4_dir_path.is_absolute():
        uv4_dir_path = (REPO_ROOT / uv4_dir_path).resolve()
    uvision = uv4_dir_path / "uVision.com"
    if not uvision.is_file():
        raise SystemExit(f"uVision.com not found: {uvision}")
    return uvision.resolve()


def hidden_process_options() -> dict[str, object]:
    options: dict[str, object] = {}
    if os.name != "nt":
        return options

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = WINDOW_HIDE
    options["startupinfo"] = startupinfo
    options["creationflags"] = subprocess.CREATE_NO_WINDOW
    return options


def run_hidden_process(cmd: list[str], cwd: Path, capture: bool = False) -> subprocess.CompletedProcess:
    options = hidden_process_options()
    if capture:
        return subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding=locale.getpreferredencoding(False),
            errors="replace",
            **options,
        )
    return subprocess.run(cmd, cwd=cwd, **options)


def run_uv4(
    uv4: Path,
    action: str,
    project_path: Path,
    target: str,
    log_path: Path,
) -> int:
    cmd = [
        str(uv4),
        action,
        str(project_path),
        "-t",
        target,
        "-o",
        str(log_path),
    ]
    print("run:", " ".join(f'"{arg}"' if " " in arg else arg for arg in cmd))
    proc = run_hidden_process(cmd, cwd=project_path.parent)
    print()
    return proc.returncode


def parse_build_result(log_path: Path) -> tuple[int | None, int | None]:
    if not log_path.exists():
        return None, None
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    matches = re.findall(r"(\d+)\s+Error\(s\),\s+(\d+)\s+Warning\(s\)", text)
    if not matches:
        return None, None
    errors, warnings = matches[-1]
    return int(errors), int(warnings)


def print_log_tail(log_path: Path, lines: int = 40) -> None:
    if not log_path.exists():
        print(f"log not found: {log_path}")
        return
    content = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    print(f"--- {log_path} tail ---")
    for line in content[-lines:]:
        print(line)


def ensure_project_and_target(
    project: Path | None,
    target: str | None,
    search_root: Path,
) -> tuple[Path, ET.Element, str]:
    project_path = project.resolve() if project else find_project_file(search_root)
    root = load_project(project_path)
    target_elem = find_target(root, target, project_path)
    return project_path, target_elem, target_name(target_elem)
