"""Verification runners for ``make verify-*`` targets.

Each module wraps a long-running command (``make deploy-all``,
``make destroy-all``, e2e pytest gate) so the recipe stays a single
``uv run python -m scripts.verify.<name>`` line in the Makefile.

The shared helper in ``_runner`` handles:

- timestamped log under ``logs/verification/<label>-YYYYMMDDTHHMMSSZ.log``
- ``<label>.latest.log`` / ``<label>.latest.exit.txt`` symlinks
- tee semantics (stdout + stderr → log file and console)
- exit-code propagation
"""
