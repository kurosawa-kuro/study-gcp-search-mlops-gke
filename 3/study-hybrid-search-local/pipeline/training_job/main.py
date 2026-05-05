"""Phase 3 — LightGBM LambdaRank training job (CLI wrapper).

CLI: ``python -m pipeline.training_job.main``

ranking_log テーブルから学習データを構築する想定だが、Phase 3 初期 (seed 完了直後)
は ranking_log がほぼ空なので、``ml.training.trainer.run`` のフォールバック
(synthetic_ranking_frames) で動かす。

Phase 4 で BigQuery loader / Cloud Run Jobs に差し替える際、本ファイルが
trainer の orchestrator として残る (Phase 7 では KFP component から呼ばれる)。

------------------------------------------------------------------------------
⚠️ TODO Wave 7 (canonical 死守ライン、User 指示 2026-05-05): 正解データ → LightGBM 接続実装
------------------------------------------------------------------------------
現状この main は ``run(df=None)`` で synthetic 経路に常時流しており、Phase 3 で
集めた ``ranking_log`` / ``ranking_labels`` / ``feedback_events`` は LightGBM 学習
に届いていない (= NDCG@10=0.9822 は乱数の in-distribution 評価)。

Wave 7 で以下を実装する:

1. ``ml/data/loaders/postgres_ranker_repository.py`` を新設 (Phase 7 既存
   ``ranker_repository.py`` の BigQuery 版パターンを踏襲、Phase 3 では PostgreSQL
   から ``ranking_labels`` × ``feature_mart_property_features_daily`` ×
   ``search_impressions`` を SQL JOIN して pandas DataFrame を返す)。

2. 本 main を以下の構造に書き換え:

       from ml.data.loaders.postgres_ranker_repository import PostgresRankerRepository

       repo = PostgresRankerRepository(dsn=settings.postgres_dsn)
       df = repo.read_training_data(since=settings.training_since)
       if df.empty:
           # ranking_labels が空 (= Wave 5-6 未起動) のときだけ synthetic に fallback
           logger.warning("ranking_labels empty; falling back to synthetic. Run `make label` first.")
           result = run(artifacts_root=artifacts_root, df=None, hp=hp)
       else:
           result = run(artifacts_root=artifacts_root, df=df, hp=hp)  # 実 ranking_labels で学習

3. ``trainer.py`` 自体は最小改修 (synthetic 経路を ``--synthetic`` フラグ / CI
   専用に分離)。``run(df=実 df)`` 経路は既に実装済 (``split_by_request_id``)。

詳細仕様は Phase 3 ``docs/02_移行ロードマップ.md §0 不変ルール 0 + §5 Wave 7``。
Wave 7 完了前は「ウェブアプリログ → BigQuery (Phase 4) 連動してもモデル改善に
繋がらない」ため canonical 死守ライン (= 「別 sprint 候補」「Wave 8 後追い」
「Phase 4 で実装」等で逃さない)。
"""

from __future__ import annotations

import os
from pathlib import Path

from ml.common import get_logger
from ml.common.config import TrainSettings
from ml.training.trainer import HyperParams, run

logger = get_logger("pipeline.training_job")


def main() -> None:
    settings = TrainSettings()
    artifacts_root = Path(os.environ.get("MODEL_ARTIFACTS_ROOT", settings.model_artifacts_root))
    if not artifacts_root.is_absolute():
        artifacts_root = Path("/app") / artifacts_root

    hp = HyperParams(
        num_leaves=settings.num_leaves,
        learning_rate=settings.learning_rate,
        num_boost_round=settings.num_boost_round,
        early_stopping_rounds=settings.early_stopping_rounds,
    )

    logger.info(
        "Phase 3 training_job start: artifacts_root=%s num_boost_round=%d",
        artifacts_root,
        hp.num_boost_round,
    )

    # Phase 3 初期は ranking_log が空 / 浅いので合成 fallback で確実に学習を一周させる。
    # Phase 4 以降で Postgres / BQ ranking_log を loader 経由で渡す。
    result = run(artifacts_root=artifacts_root, df=None, hp=hp)

    logger.info(
        "Phase 3 training_job done: run_id=%s metrics=%s train_rows=%d eval_rows=%d",
        result.run_id,
        result.metrics,
        result.num_train_rows,
        result.num_eval_rows,
    )


if __name__ == "__main__":
    main()
