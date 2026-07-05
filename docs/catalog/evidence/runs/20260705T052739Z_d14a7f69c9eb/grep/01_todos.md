# grep: todos

evidence_id: ev.grep.todos
description: TODO / FIXME / HACK comments

- app/container/internal/optional_adapter.py:L40: ``None``; handlers branch on ``container.xxx is None`` to surface 503
- pipeline/batch_serving_job/main.py:L28: """Batch serving pipeline — TODO: wire real components."""
- pipeline/evaluation_job/main.py:L28: """Evaluation pipeline — TODO: wire real components."""
- system_map.json:L836: "responsibility": "STUB KFP `property-search-evaluate` pipeline — TODO: wire real components for offline NDCG@10 / MAP / Recall@20 vs prod baseline.",
- system_map.json:L846: "responsibility": "STUB KFP `property-search-batch-serve` — TODO: wire Vertex Batch Prediction + cache hydration.",
- tests/unit/app/test_optional_adapter_helper.py:L3: The helper centralises the ``enable_xxx`` guard used by optional
