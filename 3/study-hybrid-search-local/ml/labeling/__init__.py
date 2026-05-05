"""Pure labeling logic shared across Phase 3-7."""

from .policy import ACTION_WEIGHTS, compute_label
from .synthetic_injector import SyntheticRule, inject_synthetic_labels

__all__ = [
    "ACTION_WEIGHTS",
    "SyntheticRule",
    "compute_label",
    "inject_synthetic_labels",
]
