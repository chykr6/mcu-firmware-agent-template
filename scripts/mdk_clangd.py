#!/usr/bin/env python3
"""Generate clangd files from a Keil MDK .uvprojx project.

The script does not require Keil or keil2clangd.exe. It reads the .uvprojx XML
directly, extracts the active target's C files, defines, and include paths, then
writes .clangd and compile_commands.json at the repository top level.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import sys
import xml.etree.ElementTree as ET

from mdk_common import load_toolchain


C_FILE_TYPES = {"1"}
C_SUFFIXES = {".c"}
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
CPU_NAMES = {
    "cortex-m0": "cortex-m0",
    "cortex-m0+": "cortex-m0plus",
    "cortex-m3": "cortex-m3",
    "cortex-m4": "cortex-m4",
    "cortex-m7": "cortex-m7",
    "cortex-m23": "cortex-m23",
    "cortex-m33": "cortex-m33",
}


def elem_text(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return "".join(elem.itertext()).strip()


def split_keil_list(value: str) -> list[str]:
    value = value.replace("\n", "").replace("\r", "")
    return [item.strip() for item in re.split(r"[;,]", value) if item.strip()]


def resolve_mdk_path(project_dir: Path, value: str) -> Path | None:
    value = value.strip().strip('"')
    if not value or value.startswith("$$"):
        return None

    value = value.replace("\\", os.sep)
    path = Path(value)
    if not path.is_absolute():
        path = project_dir / path
    return path.resolve()


def collect_targets(root: ET.Element) -> list[ET.Element]:
    return root.findall(".//Target")


def target_name(target: ET.Element) -> str:
    return elem_text(target.find("TargetName"))


def find_target(root: ET.Element, requested: str | None, project_path: Path) -> ET.Element:
    targets = collect_targets(root)
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


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def find_project_file(search_root: Path) -> Path:
    candidates: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(search_root):
        dirnames[:] = [
            name for name in dirnames if name not in IGNORED_SEARCH_DIRS
        ]
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


def repository_root(script_path: Path = Path(__file__)) -> Path:
    return script_path.resolve().parent.parent


def get_various_controls(target: ET.Element) -> ET.Element | None:
    cads = target.find("./TargetOption/TargetArmAds/Cads")
    if cads is None:
        return None
    return cads.find("VariousControls")


def collect_sources(project_dir: Path, target: ET.Element) -> tuple[list[Path], list[str]]:
    sources: list[Path] = []
    warnings: list[str] = []
    seen: set[Path] = set()

    for file_elem in target.findall(".//File"):
        file_type = elem_text(file_elem.find("FileType"))
        file_path_text = elem_text(file_elem.find("FilePath"))
        resolved = resolve_mdk_path(project_dir, file_path_text)
        if resolved is None:
            continue
        if file_type not in C_FILE_TYPES and resolved.suffix.lower() not in C_SUFFIXES:
            continue
        if resolved.suffix.lower() not in C_SUFFIXES:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if not resolved.exists():
            warnings.append(f"missing source: {resolved}")
            continue
        sources.append(resolved)

    return sources, warnings


def collect_defines(controls: ET.Element | None) -> list[str]:
    if controls is None:
        return []
    defines = split_keil_list(elem_text(controls.find("Define")))
    return [define for define in defines if define]


def collect_include_paths(project_dir: Path, controls: ET.Element | None) -> tuple[list[Path], list[str]]:
    if controls is None:
        return [], []

    paths: list[Path] = []
    warnings: list[str] = []
    seen: set[Path] = set()

    for include_text in split_keil_list(elem_text(controls.find("IncludePath"))):
        resolved = resolve_mdk_path(project_dir, include_text)
        if resolved is None:
            warnings.append(f"skipped unsupported include path: {include_text}")
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if not resolved.exists():
            warnings.append(f"missing include path: {resolved}")
            continue
        paths.append(resolved)

    return paths, warnings


def collect_misc_args(controls: ET.Element | None) -> list[str]:
    if controls is None:
        return []
    misc = elem_text(controls.find("MiscControls"))
    if not misc:
        return []
    return shlex.split(misc, posix=False)


def collect_cpu_args(target: ET.Element) -> tuple[list[str], list[str]]:
    common = target.find("./TargetOption/TargetCommonOption")
    cpu_text = elem_text(common.find("Cpu")) if common is not None else ""
    warnings: list[str] = []
    args: list[str] = []

    match = re.search(r'CPUTYPE\("([^"]+)"\)', cpu_text)
    cpu_name = match.group(1).strip().lower() if match else ""
    clang_cpu = CPU_NAMES.get(cpu_name)
    if clang_cpu:
        args.append(f"-mcpu={clang_cpu}")
    else:
        warnings.append(f"unsupported or missing MDK CPU type: {cpu_name or cpu_text}")

    args.append("-mthumb")
    if "FPU2" in cpu_text:
        if clang_cpu == "cortex-m4":
            args.extend(["-mfpu=fpv4-sp-d16", "-mfloat-abi=hard"])
        else:
            warnings.append(f"FPU2 mapping is unknown for CPU: {cpu_name or 'unknown'}")
    return args, warnings


def clangd_settings(config: dict, compiler_override: str | None) -> tuple[str, list[str]]:
    clangd = config.get("clangd", {})
    compiler = compiler_override or str(clangd.get("binary", "clang")).strip() or "clang"
    extra_flags = clangd.get("extra_flags", [])
    if not isinstance(extra_flags, list) or not all(
        isinstance(flag, str) for flag in extra_flags
    ):
        raise SystemExit("toolchain.local.json clangd.extra_flags must be a string list")
    return compiler, list(extra_flags)


def make_base_args(
    compiler: str,
    cpu_args: list[str],
    defines: list[str],
    includes: list[Path],
    misc_args: list[str],
    extra_flags: list[str],
) -> list[str]:
    args = [
        compiler,
        "--target=arm-none-eabi",
        "-Wall",
        "-Wno-unknown-pragmas",
        "-Wno-unused-command-line-argument",
    ]
    args.extend(cpu_args)
    args.extend(f"-D{define}" for define in defines)
    args.extend(f"-I{path}" for path in includes)
    args.extend(misc_args)
    args.extend(extra_flags)
    return args


def write_compile_commands(
    output_path: Path,
    repo_root: Path,
    base_args: list[str],
    sources: list[Path],
) -> None:
    database = []
    for source in sources:
        database.append(
            {
                "directory": str(repo_root),
                "file": str(source),
                "arguments": [*base_args, "-c", str(source)],
            }
        )

    output_path.write_text(
        json.dumps(database, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_clangd_config(repo_root: Path) -> Path:
    clangd_path = repo_root / ".clangd"
    content = """CompileFlags:
  CompilationDatabase: .

# Keep diagnostics quiet because Keil ARMCC5 and clang do not parse all vendor
# extensions identically. Code navigation and completion still use the generated
# compile_commands.json.
Diagnostics:
  Suppress: ["*"]

Index:
  Background: Build

Completion:
  AllScopes: true
"""
    clangd_path.write_text(content, encoding="utf-8")
    return clangd_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate clangd files from Keil .uvprojx."
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="Path to a .uvprojx file. If omitted, the script searches from --search-root.",
    )
    parser.add_argument(
        "--search-root",
        type=Path,
        default=Path.cwd(),
        help="Directory used to auto-discover a .uvprojx file.",
    )
    parser.add_argument(
        "--target",
        help="Keil target name. If omitted, the script auto-selects when unambiguous.",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        help="Directory where compile_commands.json and .clangd are written.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("compile_commands.json"),
        help="Output path. Relative paths are resolved from the workspace root.",
    )
    parser.add_argument("--compiler", help="override clangd.binary from toolchain config")
    parser.add_argument("--no-clangd", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    config = load_toolchain()
    compiler, extra_flags = clangd_settings(config, args.compiler)
    search_root = args.search_root.resolve()
    project_path = args.project.resolve() if args.project else find_project_file(search_root)
    if not project_path.exists():
        print(f"error: project file not found: {project_path}", file=sys.stderr)
        return 2

    workspace_root = (
        args.workspace_root.resolve()
        if args.workspace_root
        else repository_root()
    )
    project_dir = project_path.parent
    root = ET.parse(project_path).getroot()
    target = find_target(root, args.target, project_path)
    selected_target = target_name(target)
    controls = get_various_controls(target)

    sources, source_warnings = collect_sources(project_dir, target)
    defines = collect_defines(controls)
    includes, include_warnings = collect_include_paths(project_dir, controls)
    misc_args = collect_misc_args(controls)
    cpu_args, cpu_warnings = collect_cpu_args(target)
    base_args = make_base_args(
        compiler,
        cpu_args,
        defines,
        includes,
        misc_args,
        extra_flags,
    )

    output_path = args.output
    if not output_path.is_absolute():
        output_path = workspace_root / output_path
    output_path = output_path.resolve()
    write_compile_commands(output_path, workspace_root, base_args, sources)

    clangd_path = None
    if not args.no_clangd:
        clangd_path = write_clangd_config(workspace_root)

    for warning in [*source_warnings, *include_warnings, *cpu_warnings]:
        print(f"warning: {warning}", file=sys.stderr)

    print(f"project: {project_path}")
    print(f"target: {selected_target}")
    print(f"workspace root: {workspace_root}")
    print(f"sources: {len(sources)}")
    print(f"defines: {len(defines)}")
    print(f"include paths: {len(includes)}")
    if clangd_path is not None:
        print(f"wrote: {clangd_path}")
    print(f"wrote: {output_path}")
    if not sources:
        print("error: no C sources found in project", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
