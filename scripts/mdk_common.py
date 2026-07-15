from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def project_root() -> Path:
    return ROOT
