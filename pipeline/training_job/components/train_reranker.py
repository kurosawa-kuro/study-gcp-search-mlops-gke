"""KFP container component for LambdaRank training.

Wave 4 死守ライン (canonical 死守):
    本 component は **load_features が書き出した Parquet (real BigQuery
    `ranking_labels` 由来) を読み込み LightGBM LambdaRank を訓練する**。
    旧 stub (JSON metadata のみ書き出し) を撤去。

訓練は KFP component 内で `packages_to_install` 経由で lightgbm を入れて
直接実行する (Vertex AI Custom Job 経由で trainer_image を spawn する正式系は
将来 sprint で追加可能)。`trainer_image` パラメータは現状 metadata 用に保持。
`mlops.training_runs` への BQ 書き込みは Composer DAG 側で別途行う。
"""

from kfp import dsl


@dsl.component(
    base_image="python:3.12",
    packages_to_install=[
        "lightgbm>=4.5,<5.0",
        "numpy>=1.26,<3.0",
        "pandas>=2.2,<3.0",
        "pyarrow>=18.0,<22.0",
        "scikit-learn>=1.5,<2.0",
    ],
)
def train_reranker(
    trainer_image: str,
    training_frame: dsl.Input[dsl.Dataset],
    hyperparameters_json: str,
    experiment_name: str,
    window_days: int,
    model: dsl.Output[dsl.Model],
    metrics: dsl.Output[dsl.Metrics],
) -> str:
    """Read Parquet training frame → fit LambdaRank → write model + metrics.

    Returns the resolved model URI as a string so downstream components can
    consume it without relying on Input[Artifact] deserialization (KFP
    executor has historically dropped large Input[Model] payloads silently).
    """

    import json
    import sys
    import traceback
    from pathlib import Path

    def _log(msg: str) -> None:
        print(f"[train_reranker] {msg}", flush=True)
        print(f"[train_reranker] {msg}", file=sys.stderr, flush=True)

    _log("STEP 1 — component entry")
    _log(f"  python={sys.version}")
    _log(f"  trainer_image={trainer_image}")
    _log(f"  experiment_name={experiment_name} window_days={window_days}")
    _log(f"  training_frame.uri={training_frame.uri}")
    _log(f"  training_frame.path={training_frame.path}")
    _log(f"  model.uri={model.uri} model.path={model.path}")
    _log(f"  metrics.uri={metrics.uri} metrics.path={metrics.path}")

    try:
        import lightgbm as lgb
        import numpy as np
        import pandas as pd

        # 6 canonical 場所と一致させる feature column 集合 (canonical = ml/data/feature_engineering/schema.py)。
        feature_cols: list[str] = [
            "rent",
            "walk_min",
            "age_years",
            "area_m2",
            "ctr",
            "fav_rate",
            "inquiry_rate",
            "me5_score",
            "lexical_rank",
            "semantic_rank",
        ]
        group_col = "request_id"
        label_col = "label"

        _log("STEP 2 — read Parquet training frame")
        df: pd.DataFrame = pd.read_parquet(training_frame.path)
        _log(f"  rows={len(df)} columns={list(df.columns)}")
        if df.empty:
            raise RuntimeError(
                "Empty training frame from load_features — check ranking_labels coverage / window_days."
            )

        # 80/20 split by request_id (FARM_FINGERPRINT 相当を Python 側で再現)。
        # contiguous な group を維持するため、df は既に request_id x rank 順に sort 済の前提。
        _log("STEP 3 — train/test split by request_id")
        unique_ids = df[group_col].unique()
        rng = np.random.default_rng(seed=42)
        shuffled = rng.permutation(unique_ids)
        cutoff = max(1, int(len(shuffled) * 0.8))
        train_ids = set(shuffled[:cutoff])
        train_df = df[df[group_col].isin(train_ids)].reset_index(drop=True)
        test_df = df[~df[group_col].isin(train_ids)].reset_index(drop=True)
        _log(f"  train_rows={len(train_df)} test_rows={len(test_df)}")

        if len(test_df) == 0:
            test_df = train_df.copy()
            _log("  (test set empty after split — using train as eval to allow training)")

        _log("STEP 4 — build LightGBM datasets")
        train_groups = train_df.groupby(group_col, sort=False).size().to_numpy()
        test_groups = test_df.groupby(group_col, sort=False).size().to_numpy()
        train_dataset = lgb.Dataset(
            train_df[feature_cols],
            label=train_df[label_col],
            group=train_groups,
        )
        test_dataset = lgb.Dataset(
            test_df[feature_cols],
            label=test_df[label_col],
            group=test_groups,
            reference=train_dataset,
        )

        _log("STEP 5 — parse hyperparameters")
        baseline = {
            "num_leaves": 31,
            "learning_rate": 0.05,
            "feature_fraction": 0.9,
            "bagging_fraction": 0.8,
            "bagging_freq": 5,
            "min_data_in_leaf": 50,
            "lambdarank_truncation_level": 20,
        }
        try:
            override = json.loads(hyperparameters_json) if hyperparameters_json else {}
        except json.JSONDecodeError as exc:
            _log(f"WARNING — invalid hyperparameters_json: {exc}; using baseline")
            override = {}
        params = {
            "objective": "lambdarank",
            "metric": ["ndcg"],
            "ndcg_eval_at": [5, 10, 20],
            "verbose": -1,
            **baseline,
            **override,
        }
        _log(f"  params={params}")

        _log("STEP 6 — fit LambdaRank")
        booster = lgb.train(
            params,
            train_dataset,
            num_boost_round=300,
            valid_sets=[test_dataset],
            callbacks=[lgb.early_stopping(20, verbose=False)],
        )

        _log("STEP 7 — write model.txt to model.path")
        Path(model.path).parent.mkdir(parents=True, exist_ok=True)
        booster.save_model(str(model.path))
        _log(f"  wrote {Path(model.path).stat().st_size} bytes")

        _log("STEP 8 — compute eval metrics")
        # LightGBM best_score is a nested dict: {dataset_name: {metric_name: value}}.
        best_scores = dict(booster.best_score) if booster.best_score else {}
        valid_scores = next(iter(best_scores.values()), {}) if best_scores else {}
        metric_payload: dict[str, float] = {
            "ndcg_at_5": float(valid_scores.get("ndcg@5", 0.0)),
            "ndcg_at_10": float(valid_scores.get("ndcg@10", 0.0)),
            "ndcg_at_20": float(valid_scores.get("ndcg@20", 0.0)),
            "best_iteration": float(booster.best_iteration or 0),
            "train_rows": float(len(train_df)),
            "test_rows": float(len(test_df)),
        }
        Path(metrics.path).parent.mkdir(parents=True, exist_ok=True)
        Path(metrics.path).write_text(
            json.dumps(metric_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        _log(f"  metrics={metric_payload}")

        # KFP UI / Vertex Pipelines lineage に補助情報を付与。
        model.metadata.update(
            {
                "trainer_image": trainer_image,
                "training_frame_uri": training_frame.uri,
                "experiment_name": experiment_name,
                "window_days": int(window_days),
                "feature_cols": feature_cols,
                "best_iteration": int(booster.best_iteration or 0),
            }
        )

        _log(f"DONE — returning model.uri={model.uri}")
        return str(model.uri)
    except Exception:
        _log("ERROR in train_reranker")
        _log(traceback.format_exc())
        raise
