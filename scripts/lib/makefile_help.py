"""Format ``make help`` output (replaces inline awk in the Makefile).

Reads each Makefile listed on argv and prints, for every line of the
form ``<target>: ... ## <description>``, a colourised two-column
listing matching the legacy awk output.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_TARGET_RE = re.compile(r"^([a-zA-Z0-9_-]+):.*##\s*(.*)$")
_LABEL_WIDTH = 26


def _format(target: str, description: str) -> str:
    return f"  \033[36m{target:<{_LABEL_WIDTH}}\033[0m {description}".rstrip()


def main(argv: list[str] | None = None) -> int:
    paths = [Path(p) for p in (argv or sys.argv[1:])]
    print("First-time setup:  see README.md §セットアップ (run 'make doctor' to verify tools)")
    print("Quick start:       make sync-app && make verify-local-app")
    print()
    print("Targets:")
    for path in paths:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            match = _TARGET_RE.match(raw)
            if match:
                print(_format(match.group(1), match.group(2)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
