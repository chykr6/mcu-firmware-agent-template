import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional, Set

from mdk_common import ConfigError
from mdk_common import ensure_file
from mdk_common import load_config
from mdk_common import mdk_project_path
from mdk_common import mdk_target_name
from mdk_common import project_root
from mdk_common import rel_to_root


C_SUFFIXES = {".c"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate clangd files from a Keil MDK project.")
    parser.add_argument("--config", type=Path, help="toolchain config path")
    parser.add_argument("--target", help="override MDK target name")
    parser.add_argument("--compiler", default="clang", help="compiler name used in compile_commands.json")
    return parser.parse_args()


def node_name(node: ET.Element) -> str:
    return node.tag.rsplit("}", 1)[-1]


def child(node: ET.Element, name: str) -> Optional[ET.Element]:
    for item in list(node):
        if node_name(item) == name:
            return item
    return None


def text_of(node: Optional[ET.Element]) -> str:
    if node is None or node.text is None:
        return ""
    return node.text.strip()


def descendants(node: ET.Element, name: str) -> List[ET.Element]:
    return [item for item in node.iter() if node_name(item) == name]


def split_list(value: str) -> List[str]:
    parts = re.split(r"[;,]", value or "")
    return [part.strip() for part in parts if part.strip()]


def append_unique(items: List[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def resolve_project_path(project_dir: Path, value: str) -> Path:
    path = Path(value.replace("\\", "/"))
    if path.is_absolute():
        return path.resolve()
    return (project_dir / path).resolve()


def find_target(root: ET.Element, target_name: str) -> ET.Element:
    for target in descendants(root, "Target"):
        name = text_of(child(target, "TargetName"))
        if name == target_name:
            return target
    raise ConfigError(f"MDK target not found: {target_name}")


def collect_target_flags(target: ET.Element, project_dir: Path) -> List[str]:
    defines: List[str] = []
    includes: List[str] = []

    for define_node in descendants(target, "Define"):
        for define in split_list(text_of(define_node)):
            append_unique(defines, define)

    for include_node in descendants(target, "IncludePath"):
        for include in split_list(text_of(include_node)):
            include_path = str(resolve_project_path(project_dir, include))
            append_unique(includes, include_path)

    flags = ["-xc", "-std=c99"]
    flags.extend(f"-D{define}" for define in defines)
    for include in includes:
        flags.extend(["-I", include])
    return flags


def collect_source_files(root: ET.Element, project_dir: Path) -> List[Path]:
    files: List[Path] = []
    seen: Set[Path] = set()

    for file_node in descendants(root, "File"):
        path_text = text_of(child(file_node, "FilePath"))
        if not path_text:
            continue
        path = resolve_project_path(project_dir, path_text)
        if path.suffix.lower() not in C_SUFFIXES:
            continue
        if path in seen:
            continue
        seen.add(path)
        files.append(path)

    return files


def write_clangd(project_dir: Path) -> None:
    content = "CompileFlags:\n  CompilationDatabase: " + rel_to_root(project_dir) + "\n"
    (project_root() / ".clangd").write_text(content, encoding="utf-8")


def generate_compile_commands(project: Path, target_name: str, compiler: str) -> Path:
    ensure_file(project, "MDK project")
    project_dir = project.parent
    root = ET.parse(project).getroot()
    target = find_target(root, target_name)
    flags = collect_target_flags(target, project_dir)
    files = collect_source_files(root, project_dir)

    commands = []
    for source in files:
        commands.append({
            "directory": str(project_dir),
            "file": str(source),
            "arguments": [compiler, *flags, "-c", str(source)],
        })

    out = project_dir / "compile_commands.json"
    out.write_text(json.dumps(commands, indent=2), encoding="utf-8")
    write_clangd(project_dir)
    return out


def main() -> int:
    args = parse_args()
    try:
        cfg = load_config(args.config)
        project = mdk_project_path(cfg)
        target = args.target or mdk_target_name(cfg)
        out = generate_compile_commands(project, target, args.compiler)
        print(f"generated: {out}")
        return 0
    except ConfigError as exc:
        print(f"error: {exc}")
        return 2
    except ET.ParseError as exc:
        print(f"error: invalid uvprojx xml: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
