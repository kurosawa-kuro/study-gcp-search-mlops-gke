"""Run ``make deploy-all`` and aggregate output under ``logs/verification/``."""

from __future__ import annotations

from scripts.verify._runner import run


def main() -> int:
    return run("deploy-all", ["make", "deploy-all"])


if __name__ == "__main__":
    raise SystemExit(main())
