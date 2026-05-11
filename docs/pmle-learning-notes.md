# PMLE 学習ノート (実体験エビデンス起点)

本書は **Google Cloud Professional Machine Learning Engineer (PMLE) 試験** の学習を、本リポで踏破した実体験から記述する。暗記学習を体験記憶に変換するための「事例 → 試験範囲 → 一般化」の対応表。

---

## 0. なぜ実体験起点か

PMLE は概念暗記で 6 割は取れるが、合格ライン (70-80%) を超えるには「**managed vs self-hosted の比較判断**」「**コスト設計**」「**production 化の境界判断**」を実体験で持つ必要がある。本リポの 2026-05-09/10 incident 群はその素材。

---

## 1. ECK on GKE vs Vertex AI managed = self-hosted の整合コスト

### 実体験 (2026-05-09/10)

ECK 8.13.4 を GKE 上に展開。2 回連続で `Phase=ApplyingChanges Health=unknown` reconcile stall。真の root cause は **2 つの構造的 bug の重ね合わせ**:

1. **NetworkPolicy 漏れ**: `elastic-system` ns ingress が許可されておらず、ECK Operator が ES pod に到達不可
2. **TLS / auth 不整合**: ECK 8.x default は HTTPS + auth 必須だが、canonical URL は HTTP (Wave 6 contract で pin 済)

これらを直すために [`infra/manifests/elasticsearch/networkpolicy.yaml`](../infra/manifests/elasticsearch/networkpolicy.yaml) と [`elasticsearch.yaml`](../infra/manifests/elasticsearch/elasticsearch.yaml) を修正。

### PMLE 試験範囲との対応

| 試験設問パターン | 本事例から導ける答え |
|---|---|
| 「self-managed open-source vs Google managed の選択」 | **TLS / auth / NetworkPolicy の整合コスト**は managed が抽象化している。学習や検索精度比較では self が有利、production 安定運用は managed が ROI 高い |
| 「Vertex AI Vector Search vs OpenSearch / Elasticsearch on GKE」 | VVS は「Index 自体は無料、deployed_index のみ課金」の非対称構造を持ち、PDCA cycle で **Index/Endpoint persistent + deployed_index のみ作り直し** = `state rm + GCP 残置` pattern が cost 最適化の鍵 |
| 「production deployment 境界」 | HTTP + anonymous は学習用、HTTPS + password auth は production の最低ライン。本リポは学習リポジトリとして HTTP + anonymous のまま (production hardening は active backlog から外し parked)、境界は contract test `test_es_manifest_pins_http_and_anonymous_auth` + `docs/backlog/production-hardening.md` で明示 |

### 一般化

> **「設定の整合性」は managed services が一番強く抽象化する領域**。self-host の利点 (細部制御 / 比較学習 / cost) と整合コスト (TLS / 認証 / network policy / version skew) のトレードオフを、設問の文脈ごとに判定する。

---

## 2. KServe on GKE vs Vertex Endpoint = serving 選択

### 実体験

KServe ISVC (`property-encoder` / `property-reranker`) を GKE 上に。T1 (verify-live-acceptance) 1 回目で **cold start 由来の TimeoutError**、warm 後の 2 回目で **22.68s で PASS**。

cold start: scale-to-zero → 1 replica までの起動が必要、初回 latency 大。

### PMLE 試験範囲との対応

| 試験設問 | 答え |
|---|---|
| 「Vertex Endpoint vs KServe」 | KServe は **scale-to-zero がデフォルト**, Vertex Endpoint は **min_replica_count >= 1 で常駐** = cold start 体験差。レイテンシ要件が厳しいなら Vertex (replicas 常駐)、cost 最優先なら KServe (scale-to-zero) |
| 「serving cold start mitigation」 | warm-up retry / pre-warming pod / `min_replica_count=1` で常駐 (cost ↑) / 別 ASIA region に複製 (latency 改善) |
| 「e2e test の安定化」 | initial probe を warm-up に使う (本リポの T1 1 回目 fail / 2 回目 PASS は **cold start 体験そのもの**) |

### 一般化

> **「scale-to-zero は cost-optimal だが latency 体験を損ねる」**。production e2e gate は warm 後測定が筋。CI で安定させるには `make ops-livez` 後の固定 sleep か polling warm-up が必要。

---

## 3. Vertex Vector Search の persistent + state rm pattern

### 実体験

destroy-all で **Index / Endpoint は state rm + GCP 残置**、`deployed_index` のみ undeploy + recreate。次回 deploy-all は `terraform import` で state 復帰、deploy 時間が **27 min → 10-15 min** に短縮。

### PMLE 試験範囲

| 試験設問 | 答え |
|---|---|
| 「Vector Search コスト最適化」 | **Index 自体 / 空 Endpoint は無料、deployed_index (replica 起動状態) のみ課金**。PDCA loop は deployed_index だけ作り直すのが筋 |
| 「Index build 時間の隠れコスト」 | 数千件以下の embedding なら数分、数百万件は数十分。本リポ実測 = stage1 で VVS deployed_index attach が 26 min 支配 |
| 「Terraform state 管理 + GCP 残置 pattern」 | `state rm` + `terraform import` の組み合わせは **terraform-managed と GCP 残置の境界**を移動できる強力なパターン。設問で「TF で管理しないが GCP に残す」要件があれば本 pattern |

---

## 4. Composer (Managed Airflow) vs Cloud Scheduler / Eventarc

### 実体験

Composer Gen 3 を **本線 retrain orchestrator** として採用。Cloud Scheduler / Eventarc / Cloud Function trigger は **smoke / manual のみ**、本線重複起動禁止。Composer 環境作成が 15-25 min、destroy も同程度。

### PMLE 試験範囲

| 試験設問 | 答え |
|---|---|
| 「Workflow orchestration 選択」 | Composer (managed Airflow) = **DAG 依存関係 / retry / SLA** が必要なら筋。Cloud Scheduler は cron 単発、Eventarc は GCS 等の event-driven。**重複起動禁止** が PDCA loop の暗黙制約 |
| 「Composer の cost 構造」 | **環境作成・常駐料金 ¥2-3k/日** + DAG 実行コスト。dev project は当日 destroy 前提 (本リポの 1.4-bis コスト見積もり) |

---

## 5. Feature Store (Vertex AI Feature Online Store) と Feature View

### 実体験

`property_features_online_latest` BigQuery view を Feature Online Store source に。Feature View 経由で KServe が `feature_fetcher` で online lookup。training-serving skew 防止。

### PMLE 試験範囲

| 試験設問 | 答え |
|---|---|
| 「training-serving skew 防止」 | 同一 schema / 同一 source の Feature を training と serving で参照。Vertex Feature Store の Feature View は **serving 接続点** |
| 「BigQuery → Feature Online Store sync」 | offline (BQ) → online (FOS) の sync 経路。manual sync trigger + completion polling が canonical (`scripts/domain/gcp/feature_view_sync.py`) |

---

## 6. SLO / Monitoring / burn-rate alert

### 実体験

Cloud Monitoring SLO + burn-rate alert を Terraform module で実装。

### PMLE 試験範囲

| 試験設問 | 答え |
|---|---|
| 「SLO で何を測る」 | latency p99 / availability (success ratio) / freshness (Feature staleness) |
| 「burn-rate alert」 | 短期 (5min, 14.4x) と長期 (1h, 6x) 2-window で fast / slow burn を区別 |

---

## 7. Workload Identity Federation (WIF) のソフトデリート 30 日

### 実体験

`make destroy-all` 後 `make deploy-all` で `Error 409: Requested entity already exists` 多発。WIF pool / provider は GCP が **30 日 soft-delete 保持**、recreate は 409。`recover_wif.py` で `undelete` + `terraform import` で吸収。

### PMLE 試験範囲

| 試験設問 | 答え |
|---|---|
| 「GitHub Actions → GCP の認証」 | service account key より WIF が推奨 |
| 「destroy → recreate 時の罠」 | IAM SA は 30 日 soft-delete、WIF pool / provider も同様。recreate は 409 → undelete + import 経路が canonical |

---

## 8. 試験対策の運用 (本書の使い方)

1. **本書を試験 1 週間前に再読**: 体験記憶のリハーサル。各 §の「PMLE 試験範囲との対応」だけでも回す
2. **不足を発見したら追記**: 試験で「あれ?」となった設問は、本リポでどう扱われていたかを §として追加
3. **公式 model questions と突合**: 本書の事例で答えられる問題と、答えられない問題を分類

---

## 関連

- 本リポ全 incident memo: [`architecture/03_実装カタログ.md §7.4`](architecture/03_実装カタログ.md)
- ECK 不整合の真の root cause: [`troubleshooting/eck-license-reconcile-stall.md`](troubleshooting/eck-license-reconcile-stall.md)
- VVS persistent design: [`tasks/TASKS_ROADMAP.md §4.9`](tasks/TASKS_ROADMAP.md)
- WIF soft-delete recovery: [`troubleshooting/eck-license-reconcile-stall.md`](troubleshooting/eck-license-reconcile-stall.md) と `scripts/setup/recover_wif.py`
