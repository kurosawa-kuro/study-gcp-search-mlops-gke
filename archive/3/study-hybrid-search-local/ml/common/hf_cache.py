"""Helpers for local-first Hugging Face / sentence-transformers loading."""

from __future__ import annotations

from pathlib import Path

from huggingface_hub import snapshot_download

from ml.common.logging import get_logger

logger = get_logger("ml.common.hf_cache")


def resolve_sentence_transformer_source(model_name: str) -> str:
    """Prefer an already-cached local snapshot over a live Hub lookup.

    When the model is present in the shared ``hf_cache`` volume, return the
    concrete snapshot path so ``SentenceTransformer(...)`` can load without the
    repeated remote HEAD checks that hurt Phase 3 startup time.
    """

    try:
        snapshot_path = snapshot_download(repo_id=model_name, local_files_only=True)
    except Exception:
        logger.info("HF cache miss for %s; fallback to live Hub resolution", model_name)
        return model_name

    resolved = str(Path(snapshot_path))
    logger.info("HF cache hit for %s -> %s", model_name, resolved)
    return resolved
