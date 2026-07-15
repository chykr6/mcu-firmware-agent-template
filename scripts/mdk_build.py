import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "toolchain.local.json"


def load_config():
    if CONFIG.exists():
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    return json.loads((ROOT / "toolchain.example.json").read_text(encoding="utf-8"))


def main():
    cfg = load_config()
    uv4 = cfg["uv4"]
    project = ROOT / cfg["project"]
    target = cfg["target"]
    log = project.parent / "build_mdk.log"
    if not project.exists():
        raise SystemExit(f"MDK project not found: {project}")
    cmd = [uv4, "-b", str(project), "-t", target, "-o", str(log)]
    print("run:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=project.parent)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
