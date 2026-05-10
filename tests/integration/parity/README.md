# tests/integration/parity/

canonical 構成 の **lock-step 不変条件** を pin する pytest 群。
"3 箇所の同じ概念がバラバラに変更され silent でデータ破損" を CI で防ぐ。

## 何を pin しているか (現行)

| test ファイル | lock-step する file 群 | 守りたい不変条件 |
|---|---|---|
| `test_codebase_invariants.py` | `app/` / `ml/` / `pipeline/` / `scripts/*.py` / `infra/manifests/**/*.yaml` ↔ `docs/runbook/04_検証.md` §2 L1'' | W2-8 互換レイヤ文字列と Meilisearch lexical 残骸が canonical コードツリーに戻らない（手動 ``rg`` の CI 代替）。インフラ cleanup 用の ``scripts/domain/gcp/state_recovery.py`` は対象外 |
| `test_feature_parity_ranking.py` | `ml/data/feature_engineering/schema.py::FEATURE_COLS_RANKER` ↔ `infra/terraform/modules/data/main.tf::ranking_log.features` ↔ `pipeline/data_job/dataform/features/property_features_daily.sqlx` | ranker 学習用の特徴量列が Python / BQ table schema / Dataform feature SQL で一致 |
| `test_feature_parity_feature_group.py` | `FEATURE_COLS_RANKER` ↔ `infra/terraform/modules/vertex/main.tf::feature_group_property_features` | Vertex Feature Group の property-side feature 順序と value_type が Python と一致 |
| `test_feature_parity_sql_ranker.py` | `FEATURE_COLS_RANKER` ↔ `infra/sql/monitoring/validate_feature_skew.sql` UNPIVOT | feature skew SQL が UNPIVOT する列が Python schema と一致 |
| `test_dataform_workflow_settings.py` | `env/config/setting.yaml` ↔ `pipeline/data_job/dataform/workflow_settings.yaml` (auto-generated) | `scripts/ci/sync_dataform.py` が出力する Dataform 設定と setting.yaml が同期 |
| `test_configmap_drift.py` | `env/config/setting.yaml` ↔ `infra/manifests/search-api/configmap.example.yaml` (auto-generated) | `scripts/ci/sync_configmap.py` が出力する ConfigMap が setting.yaml と同期 |

## 新しい parity test を **登録するかの判定基準**

以下を **すべて** 満たすときだけ追加する:

1. **同じ概念が 2 箇所以上に物理的に存在する** (DRY できない構造的理由がある — 例: Python と SQL、Python と Terraform、Python と YAML)
2. **片方だけ変更すると silent failure になる** (CI test / runtime error が即座に出ない)
3. **失敗時の被害が大きい** (data loss / schema drift / production traffic 0 / 認証突破 等)
4. **lock-step ルールを 1 行で言語化できる** (このルール文が assert message に書ける)

逆に **登録しないもの**:
- 単なるコード規約 (lint で済む) → `ruff`
- 命名一致 (rename 漏れ) → `make check-layers` の境界検査か mypy
- 1 ファイル内の整合 → 通常の unit test

## ローカル優先ゲート (offline)

- **`make verify-local-parity`** — `pytest tests/integration/parity` のみ（GCP 不要）。仕様ドキュメントとコードのズレを **parity + invariants** で早期検知する。
- **`make verify-local-hybrid`** — `verify-local-parity` → ground-truth contract → `verify-local-app` → `verify-local-ml` の順（runbook §2 の「ローカルで落とせる失敗」を Cloud に持ち込まない思想と整合）。

## 共通 helper (`parity_invariant.py`)

新 parity test は以下を **必ず** 使う (per-file 重複を避ける):

- `REPO_ROOT` — `parents[3]` 計算を repo に閉じる
- `read_text(path)` — UTF-8 読み込み (encoding を全 test で揃える)
- `flat_yaml(text)` — `setting.yaml` 系の単純な `key: value` parser
- `extract_terraform_block(text, resource_type=..., name=...)` — brace-balanced で `resource "..." "..." {}` 内部を返す
- `FEATURE_COLS_RANKER` / `PROPERTY_SIDE_COLS` / `QUERY_TIME_COLS` — ranker 特徴量列の正本 + サブセット

新規 helper を生やすときは「2 つ以上の parity test が同じパターンを持つことが確実」になってから昇格する。先回り的な helper 化は YAGNI。

## 失敗時の対応フロー

1. **どの file が canonical か** を `parity_invariant.py` のコメント or 該当 test の docstring で確認
2. canonical 側を編集
3. 派生側を canonical に合わせる (auto-generated なら `make sync-dataform-config` / `make sync-configmap` を実行)
4. test が green になるまでループ

「とりあえず派生側に合わせる」は禁則 — drift の原因がそこに焼き込まれる。
