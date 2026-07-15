import argparse
from pathlib import Path

from mdk_common import (
    ConfigError,
    ensure_file,
    load_config,
    mdk_project_path,
    mdk_target_name,
    run_command,
    tool_path,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Keil MDK target.")
    parser.add_argument("--config", type=Path, help="toolchain config path")
    parser.add_argument("--target", help="override MDK target name")
    parser.add_argument("--rebuild", action="store_true", help="use UV4 rebuild instead of build")
    parser.add_argument("--clean", action="store_true", help="clean target before build")
    parser.add_argument("--log", type=Path, help="build log path")
    return parser.parse_args()


def uv4_command(uv4: Path, project: Path, target: str, log: Path, action: str) -> list[str]:
    return [str(uv4), action, str(project), "-t", target, "-o", str(log)]


def main() -> int:
    args = parse_args()
    try:
        cfg = load_config(args.config)
        uv4 = tool_path(cfg, "uv4")
        project = mdk_project_path(cfg)
        target = args.target or mdk_target_name(cfg)
        log = args.log or (project.parent / "build_mdk.log")

        ensure_file(uv4, "UV4")
        ensure_file(project, "MDK project")
        log.parent.mkdir(parents=True, exist_ok=True)

        if args.clean:
            code = run_command(uv4_command(uv4, project, target, log, "-c"), project.parent)
            if code != 0:
                return code

        action = "-r" if args.rebuild else "-b"
        return run_command(uv4_command(uv4, project, target, log, action), project.parent)
    except ConfigError as exc:
        print(f"error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
