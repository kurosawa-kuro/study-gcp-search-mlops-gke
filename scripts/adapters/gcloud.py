"""Thin adapter around the `gcloud` CLI.

The actual implementation lives in `scripts/_common.py::gcloud` (historical
location, used by ~10 callers as of 2026-05-10). This module re-exports it so
new callers can use the canonical adapter import path:

    from scripts.adapters.gcloud import gcloud_run

Existing callers using `from scripts._common import gcloud` continue to work;
migration to the adapter import is incremental.
"""

from __future__ import annotations

from scripts._common import gcloud as gcloud_run

__all__ = ["gcloud_run"]
