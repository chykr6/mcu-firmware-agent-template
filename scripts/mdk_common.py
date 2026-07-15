import json
import subprocess
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "toolchain.example.json"
LOCAL_CONFIG = ROOT / "toolchain.local.json"


class ConfigError(Exception):
    pass


def project_root() -> Path:
    return ROOT


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid json: {path}: {exc}") from exc


def load_config(config_path: Optional[Path] = None) -> dict:
    path = config_path or LOCAL_CONFIG
    if not path.exists():
        path = DEFAULT_CONFIG
    cfg = read_json(path)
    cfg["_config_path"] = str(path)
    return cfg


def require_value(cfg: dict, key: str) -> str:
    value = str(cfg.get(key, "")).strip()
    if not value:
        raise ConfigError(f"missing toolchain field: {key}")
    return value


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def mdk_project_path(cfg: dict) -> Path:
    return resolve_repo_path(require_value(cfg, "project"))


def mdk_target_name(cfg: dict) -> str:
    return require_value(cfg, "target")


def tool_path(cfg: dict, key: str, required: bool = True) -> Optional[Path]:
    value = str(cfg.get(key, "")).strip()
    if not value:
        if required:
            raise ConfigError(f"missing toolchain field: {key}")
        return None
    return Path(value)


def ensure_file(path: Optional[Path], label: str) -> None:
    if path is None:
        raise ConfigError(f"{label} path is empty")
    if not path.exists():
        raise ConfigError(f"{label} not found: {path}")
    if not path.is_file():
        raise ConfigError(f"{label} is not a file: {path}")


def rel_to_root(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def run_command(cmd: list, cwd: Path) -> int:
    print("run:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode
