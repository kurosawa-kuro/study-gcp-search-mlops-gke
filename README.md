# study-gcp-search-mlops-gke

不動産ハイブリッド検索 + 継続改善 MLOps サイクルの個人技術学習プロジェクト。

題材は不動産検索、技術スタックは **Cloud Composer 本線 orchestration + Vertex AI Pipelines / Feature Store / Vector Search / Model Registry + GKE Deployment + KServe InferenceService + PMLE 統合技術 (BQML / Dataflow / TreeSHAP / Monitoring SLO)**。Serving 層は KServe pod から Feature Online Store を Feature View 経由で opt-in 参照する経路を持つ。

> **最初に読むファイル**:
> - [`docs/tasks/TASKS.md`](docs/tasks/TASKS.md) — current sprint
> - [`docs/architecture/01_仕様と設計.md`](docs/architecture/01_仕様と設計.md) — canonical 仕様
> - [`docs/architecture/03_実装カタログ.md`](docs/architecture/03_実装カタログ.md) — 実装スナップショット
> - [`CLAUDE.md`](CLAUDE.md) — Claude Code 向けガイド

---

## 1. プロジェクト概要

### 1.1 ゴール

検索アプリ単発ではなく **「行動ログから正解データを作り、継続的にランキングを改善できる MLOps サイクル」** を実装すること。

```
Search API / KServe serving
  ↓
event logs (search_events / search_impressions / user_actions)
  ↓
BigQuery curated
  ↓
Cloud Composer (retrain_orchestration DAG)
  ↓
labeling SQL (重み付き relevance label → ranking_labels)
  ↓
training dataset (GCS object)
  ↓
Vertex AI Pipelines (LightGBM LambdaRank retrain)
  ↓
Vertex Model Registry
  ↓
deployment gate (NDCG@10 / Recall@K / CTR / CVR 評価)
  ↓
KServe storageUri patch (新 model artifact 反映)
```

### 1.2 設計思想

- **中核 5 要素 (不変)**: Elasticsearch BM25 + multilingual-e5 + Vertex AI Vector Search + RRF + LightGBM LambdaRank
- **Port/Adapter / `core → ports ← adapters` の依存方向**: adapter 実装だけ差し替えで Local 検証 / Cloud canonical / 実案件 reference (Elasticsearch + Redis 同義語 + ME5 + Vertex Vector Search + LightGBM) に到達できる構造を維持
- **Composer × Vertex Pipelines は上下関係**: Composer = 上位 orchestrator、Vertex Pipelines = 下位 ML executor。`train/evaluate/register` を Composer 側に書かない (カニバリ禁止)

### 1.3 教材対象外

下記は導入・言及しない:

- **Agent Builder / Vizier / Model Garden / Gemini RAG** — ハイブリッド検索中核と機能カニバリを起こす、もしくは学習価値が低い
- **W&B / Looker Studio / Doppler** — 実験履歴は GCS / BigQuery / Vertex Model Registry / Vertex Pipelines Metadata で十分

---

## 2. 技術スタック

| 層 | 採用技術 |
|---|---|
| Lexical 検索 | Elasticsearch + Redis 同義語辞書 (Cloud Memorystore、`SynonymExpanderPort` + `RedisSynonymExpander`) |
| Semantic 検索 | multilingual-e5 (KServe InferenceService) + Vertex AI Vector Search (serving index) |
| 候補融合 | RRF (Reciprocal Rank Fusion) |
| Rerank | LightGBM LambdaRank (KServe InferenceService、MLServer runtime) |
| 特徴量管理 | Vertex AI Feature Store (Feature Group / Feature View / Feature Online Store、Optimized 型、training-serving skew 防止) |
| 検索ログ → BigQuery | Pub/Sub topic → BigQuery Subscription (`use_table_schema`): `ranking-log` → `mlops.ranking_log` / `search-feedback` → `mlops.feedback_events` / `search-events` → `mlops.search_events` / `search-impressions` → `mlops.search_impressions` / `user-actions` → `mlops.user_actions`。`EventWriter` canonical = `PubSubEventWriter`、3 topic 未設定時のみ `CloudLoggingEventWriter` fallback |
| 再学習 trigger | **Cloud Composer DAG** (`retrain_orchestration`、本線)。Cloud Scheduler / Eventarc / Cloud Function は smoke / manual trigger 用 |
| ML pipeline | Vertex AI Pipelines (KFP v2、`pipeline/{data_job,training_job,evaluation_job,batch_serving_job}/`) |
| モデル管理 | Vertex Model Registry (`staging` / `production` alias) |
| 監視 | Cloud Monitoring + Vertex Model Monitoring + GMP `PodMonitoring` + SLO (custom_service `k8s_service` 型) + burn-rate alert |
| serving 層 | GKE Autopilot Deployment (`search-api`) + KServe InferenceService (`property-encoder` / `property-reranker`)。公開 URL `https://gcp-search-mlops-gke.dev` |
| 公開ドメイン / TLS | Cloud Domains 取得ドメイン `gcp-search-mlops-gke.dev` + Cloud DNS public zone `gcp-search-mlops-gke-dev` + Certificate Manager (DNS-01 authorization、`networking.gke.io/certmap`) + 予約グローバル外部 IP。`.dev` TLD は HSTS preload 強制。`infra/terraform/modules/dns/`。✅ 2026-05-11 deploy + cert `managed.state=ACTIVE` + `https://.../api/v1/search` 200 確認済 |
| 認可 | Gateway API (`gke-l7-global-external-managed`) + IAP (外部) + NetworkPolicy (内部: search → kserve-inference のみ許可) |
| Secret 管理 | GCP Secret Manager + External Secrets Operator (K8s Secret 自動同期) |
| IaC | Terraform 1.9+ (14 modules) + Helm provider |
| CI/CD | GitHub Actions + Workload Identity Federation (SA Key 禁止) |
| PMLE 統合技術 | BQML popularity / Dataflow Flex Template / TreeSHAP Explainability / Monitoring SLO + burn-rate / Composer-managed BigQuery monitoring query |

---

## 3. 非負制約

詳細は [`docs/architecture/01_仕様と設計.md §0`](docs/architecture/01_仕様と設計.md)。

- **中核 5 要素の挙動・データフロー・デフォルト `/search` 応答は維持**: 置換・削減・無効化は事前の明示合意必須
- **Vertex Vector Search の役割**: ME5 ベクトル検索の本番 serving index。embedding 生成履歴・メタデータの正本は BigQuery 側 (data lake / serving index の二層構造)
- **Feature Store**: Vertex AI Feature Store により training-serving skew を防ぐ。Online Store を使う実務では **Feature View が serving 接続点**
- **Cloud Composer 本線**: Managed Airflow Gen 3 を本線オーケストレーターとして実装 (`infra/terraform/modules/composer/` + `pipeline/dags/` の 3 DAG: `daily_feature_refresh` / `retrain_orchestration` / `monitoring_validation`)。Vertex `PipelineJobSchedule` は完全撤去 (二重起動禁止)、Cloud Scheduler / Eventarc / Cloud Function trigger は smoke / manual 用に格下げ
- **Event schema 共通契約**:
  - `search_events` (`event_id` / `search_id` / `user_id` / `session_id` / `query` / `filters_json` / `timestamp` / `app_version` / `model_version`)
  - `search_impressions` (`event_id` / `search_id` / `property_id` / `rank` / `lexical_score` / `vector_score` / `rrf_score` / `rerank_score` / `timestamp`)
  - `user_actions` (`event_id` / `search_id` / `property_id` / `action_type` / `action_value` / `timestamp`)
  - `action_type` enum 8 種: アプリ emit 5 種 (`click`=1, `detail_view`=2, `favorite`=3, `request_button_click`=4, `request_complete`=5) + synthetic 注入専用 3 種 (`inquiry_complete`=7, `contract`=10, `bounce`=0/-1)
  - アプリ → BigQuery への書込みは **Pub/Sub topic → BigQuery Subscription 経由** (`PubSubEventWriter` / `PubSubFeedbackRecorder` / `PubSubRankingLogPublisher`)。`CloudLoggingEventWriter` は 3 topic 未設定時の bootstrap fallback のみ
  - synthetic 注入は `definitions/labeling/synthetic_actions.yaml` から `ranking_labels.label_source='synthetic_*'` で擬似正解データを書き込む。`ml/labeling/` は psycopg / google.cloud import 禁止で純粋ロジック維持
- **LightGBM 接続前提**: `ranking_labels` を集めても、`pipeline/training_job/main.py` から `ml/data/loaders/ranker_repository.py` (BigQuery loader) を呼ぶ配線実装が完了していない限り LightGBM 学習に流れない。**canonical 死守ライン** (詳細は [`docs/architecture/01_仕様と設計.md §8`](docs/architecture/01_仕様と設計.md))
- **実案件 reference architecture**: Elasticsearch + Redis 同義語辞書 + ME5 + Vertex Vector Search + LightGBM。教材構成も lexical lane は Elasticsearch を canonical とする
- ⚠️ **ES は学習用 (a') 解 (HTTP + anonymous superuser)**: `infra/manifests/elasticsearch/elasticsearch.yaml` は HTTP + anonymous superuser で運用 (学習プロジェクト前提の意図的設定)。production 化 (HTTPS + password auth) の手順は [`docs/backlog/production-hardening.md`](docs/backlog/production-hardening.md) を参照（active backlog からは外し parked）。**商用展開時は必ず `xpack.security.authc.anonymous.*` を無効化すること**。`test_es_manifest_pins_http_and_anonymous_auth` がこの状態を pin（= 学習用途の自己拘束）

---

## 4. リポジトリ構成

```text
.
├── README.md                  # 本ファイル
├── CLAUDE.md                  # Claude Code 向けガイド
├── AGENTS.md                  # Agent / Cursor 向けガイド (CLAUDE の英訳サブセット)
├── Makefile                   # 開発 / Terraform / E2E / ops のエントリポイント
├── pyproject.toml             # uv workspace root
├── uv.lock
├── app/                       # FastAPI search-api (GKE Deployment)
│   ├── main.py                # entrypoint (`create_app()` + lifespan)
│   ├── composition_root.py    # DI Container (frozen dataclass)
│   ├── observability.py       # metrics + logging seam
│   ├── domain/                # Candidate / SearchFilters / SearchInput / SearchOutput
│   ├── api/                   # routers / mappers / middleware / dependencies
│   ├── container/             # DI builder 分割 (infra / search / ml)
│   └── services/              # protocols / adapters / noop_adapters / search_service / ranking
├── ml/                        # 機能別 ML 実装
│   ├── common/                # 設定 + logging + run_id
│   ├── data/                  # ranker_features / loaders (BigQueryRankerRepository)
│   ├── training/              # LightGBM trainer + ports/adapters
│   ├── evaluation/            # NDCG / metrics / validators / report
│   ├── serving/               # encoder / reranker / predictor (KServe)
│   ├── streaming/             # Beam pipeline + Dataflow Flex Template
│   ├── registry/              # Vertex Model Registry ラッパ
│   └── labeling/              # 重み付き relevance label + synthetic_injector (純粋ロジック)
├── pipeline/                  # Vertex AI Pipelines + Cloud Composer DAG
│   ├── data_job/              # property-search-embed (KFP) + Dataform
│   ├── training_job/          # property-search-train (KFP)
│   ├── evaluation_job/        # property-search-evaluate
│   ├── batch_serving_job/
│   ├── workflow/              # KFP compile + Cloud Function trigger
│   └── dags/                  # Composer DAG 3 本 + _pod.py helper
├── infra/
│   ├── terraform/             # 14 modules (iam / data / messaging / monitoring / vertex / slo / streaming / vector_search / gke / kserve / composer / elasticsearch / redis_synonym / dns)
│   ├── manifests/             # K8s manifests (`kubectl apply -k`)
│   ├── sql/                   # monitoring SQL (skew / drift)
│   └── run/services/          # Cloud Build 定義 + Dockerfile (svc ごとに co-located)
├── scripts/                   # Makefile から呼ぶ Python (`{setup,deploy,ops,bqml,ci,sql}`)
├── tests/                     # `unit/` `integration/` `e2e/` + `_fakes/`
├── env/                       # `config/setting.yaml` (SSoT) + `secret/`
├── definitions/               # synonyms / labeling YAML fixture
├── tools/                     # ローカル補助 (Makefile-doc 生成、layout check)
├── logs/                      # 生成物 (deploy / verification ログ)
└── docs/                      # 仕様 / runbook / tasks / decisions / conventions
```

詳細は [`docs/architecture/03_実装カタログ.md`](docs/architecture/03_実装カタログ.md) を参照。

---

## 5. 開発フロー

### セットアップ

```bash
make doctor                    # 前提ツール確認 (uv / gcloud / kubectl / terraform)
make sync                      # uv sync (full workspace)
```

### CI 同等チェック

```bash
make check                     # ruff + ruff format --check + mypy strict + pytest
make check-layers              # AST-based Port-Adapter 境界検査
make tf-validate               # terraform validate (offline)
```

### Local 検証 (GCP に触れない)

```bash
make verify-local-app          # FastAPI boot + DI + API contract
make verify-local-ml           # ML / pipeline 単体 + smoke train
make verify-local-hybrid       # workflow contract + 上記 2 つ
```

### Cloud canonical (実 GCP)

```bash
make deploy-all                # 15 step (tf-bootstrap → 2 段階 apply → seed → elasticsearch-sync → composer-deploy-dags → deploy-api)
make run-all                   # canonical validation 16 step (= run-all-core; orchestrator: scripts/ops/run_all.py)
make destroy-all               # no-prompt teardown (8 step)
```

`deploy-all` / `run-all` / `destroy-all` は各 step の wall time を `logs/step_timings.csv` (gitignore、`flow` カラム付き) に記録し、起動時に過去 run の median から ETA + 重い step トップ3 を表示する (`scripts/lib/step_timing.py`)。詳細は [`docs/runbook/05_運用.md`](docs/runbook/05_運用.md) と [`docs/runbook/04_検証.md`](docs/runbook/04_検証.md) を参照。

> **実装状態 (2026-05-11)**: M-Wave9 公開ドメイン (`https://gcp-search-mlops-gke.dev` + Certificate Manager) **全 Step 完了** — `make deploy-all` 15/15 完走 / cert `managed.state=ACTIVE` / `make ops-search TARGET=gcp` HTTPS 200 / `make run-all-core` 16/16 完走 (`ndcg=hit_rate=mrr=1.0`)。詳細は [`docs/architecture/03_実装カタログ.md §6 / §7.3`](docs/architecture/03_実装カタログ.md)。

---

## 6. ドキュメント導線

| ディレクトリ | 内容 |
|---|---|
| [`docs/architecture/`](docs/architecture/) | 仕様 + 実装カタログ |
| [`docs/runbook/`](docs/runbook/) | 検証ゲート + 運用手順 |
| [`docs/tasks/`](docs/tasks/) | current sprint + 長期 backlog |
| [`docs/decisions/`](docs/decisions/) | ADR (恒久対処ギャップの記録、0001〜0008) |
| [`docs/conventions/`](docs/conventions/) | 命名 / 配置 / Make / Docker の規約セット |

権威順位: `tasks/TASKS_ROADMAP.md > tasks/TASKS.md > 01_仕様と設計.md > README.md > CLAUDE.md`

---

## 7. 設定とシークレット

- `env/config/setting.yaml` = 単一の設定正本 (非秘密値のみ、`project_id` / `region` / `api_service` / Vertex location / `public_domain` (`gcp-search-mlops-gke.dev`) / `dns_zone_name` (`gcp-search-mlops-gke-dev`) 等)。Makefile が awk で読んで `-var=...` を Terraform へ流す (`github_repo` / `oncall_email` / `public_domain` / `dns_zone_name` = `CANONICAL_TF_VAR_NAMES`)
- `env/secret/credential.yaml` = ローカル用の秘密値 (gitignore 対象)
- 本番 secret は GCP Secret Manager 正本 (`search-api-iap-oauth-client-secret` / `mlops-synonym-redis-auth`)、External Secrets Operator が K8s Secret に自動同期

`pydantic-settings` で `env > setting.yaml` の優先順で読む。

---

## 8. CI / IaC

- GitHub Actions (`.github/workflows/`、8 本): `ci.yml` / `terraform.yml` / `deploy-api.yml` / `deploy-dataform.yml` / `deploy-encoder-image.yml` / `deploy-reranker-image.yml` / `deploy-trainer-image.yml` / `deploy-pipeline.yml`
- 認証: Workload Identity Federation のみ (SA Key 禁止)。`sa-github-deployer` が WIF 経由で各 SA に impersonate
- Terraform: 14 modules、`tests/integration/infra/test_terraform_module_structure.py` が 4 ファイル構成 (`main.tf` / `variables.tf` / `outputs.tf` / `versions.tf`) + variable description を構造検証

---

## 9. 検証 (G-W1〜G-W6 ゴール契約)

`tests/integration/workflow/` と `tests/e2e/` が将来にわたり固定する到達ゴール。詳細は [`docs/architecture/01_仕様と設計.md §9`](docs/architecture/01_仕様と設計.md)。

- **G-W1**: PDCA は `deploy-all → run-all → destroy-all` の 1 本線で完結する
- **G-W2**: deploy 本線は seed 後に online serving 側の同期が走る
- **G-W3**: runtime 設定は生成物ではなく canonical source から復元できる
- **G-W4**: canonical serving path (lexical / semantic / rerank / Feature View 経由 fetch) を検証本線に含める
- **G-W5**: failure は必ず診断可能である
- **G-W6**: destroy は「壊す」だけでなく次 cycle の再現性も守る

「OK」の判定は **API 200 ではなく**、3 系統 all non-zero + Vertex Vector Search 実検索 + Feature View 経由 fetch + KServe 経由 rerank + 継続改善サイクル完走 (deployment gate 評価で promote 判定が出て、KServe storageUri が新 model artifact を指すまで) を含む。
