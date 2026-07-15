#!/usr/bin/env python3
import re
import sys
from pathlib import Path

HEADER_RE = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9_-]+\))?: .{1,72}$")


def main() -> int:
    msg_path = Path(sys.argv[1])
    lines = msg_path.read_text(encoding="utf-8").splitlines()
    meaningful = [line for line in lines if not line.startswith("#")]
    if not meaningful or not HEADER_RE.match(meaningful[0]):
        print("commit-msg: first line must be Conventional Commits, <=72 chars", file=sys.stderr)
        return 1
    if len(meaningful) > 1:
        if meaningful[1] != "":
            print("commit-msg: second line must be blank when body exists", file=sys.stderr)
            return 1
        body = meaningful[2:]
        for line in body:
            if line and not line.startswith("- ") and not line.startswith("BREAKING CHANGE:"):
                print("commit-msg: body lines must use '- ' bullets", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
