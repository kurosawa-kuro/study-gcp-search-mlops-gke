"""Run ``make destroy-all`` and aggregate output under ``logs/verification/``."""

from __future__ import annotations

from scripts.verify._runner import run


def main() -> int:
    return run("destroy-all", ["make", "destroy-all"])


if __name__ == "__main__":
    raise SystemExit(main())
