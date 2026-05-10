# TASKS_ROADMAP

不動産ハイブリッド検索 + 継続改善 MLOps サイクルの **長期 backlog + 不変ルール + 残 Wave の母艦**。

権威順位: `TASKS_ROADMAP > TASKS > 01_仕様と設計 > README > CLAUDE`

完了済の実装ログ / マイルストーン履歴 / incident memo は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §6 (直近完了ログ) / §7.3 (マイルストーン履歴) / §7.4 (incident memo) を正本とする。本書は **未完了 / 残課題 / 不変ルール** のみ残す。

---

## §0. プロジェクト方針

### §0.1 ピボット完了 + Phase 概念完全撤廃 (M-Wave8.5、2026-05-10)

教育用 Phase 1〜7 形式は廃止、個人技術学習プロジェクトに pivot。`Phase [0-9]` キャピタル P 表記は docs / tests から完全撤去。

例外:
- ADR (`docs/decisions/`) は historical record として `Phase X` 表記を残置 (retroactive note は ADR README に明記)
- e2e test ファイル名 (`tests/e2e/test_phase7_*.py` / `live_acceptance_checks.py::test_phase7_*`) は historical fixture として残置 (rename すると fixture と手元の運用ログ参照が drift する)
- M-Wave マイルストーンの Phase 1/2/3 (M-Wave8.6 Phase 1/2/3 等) は milestone 段階の固有名 = 撤廃対象外
- GCP リソース ID は **2026-05-10 rename 済**: `phase7-synonym` → `mlops-synonym` (Memorystore + Secret + ExternalSecret); Make target `destroy-phase7-learning` → `destroy-coast-down`; Docker tag `phase7-ml-base:local` → `mlops-ml-base:local`

### §0.2 仕様の大本命 (正解データ + 継続改善サイクル)

行動ログ → 正解データ → 再学習 → 評価 → deployment gate → KServe 反映 を 1 本の継続改善サイクルとして実装。アプリ側 (EventWriter Port) とモデル側 (`pipeline/training_job/main.py` の Repository 配線) の両方で正解データ対応。**M-Wave5 で 2026-05-10 完了**。

### §0.3 検索基盤 (Elasticsearch on GKE)

Meilisearch を廃止、GKE 上で Elasticsearch (ECK) を稼働。Elastic Cloud は不採用。**M-Wave6 で完了**、**M-Wave8.7 で HTTPS+password auth へ production 化** (backlog)。

---

## §1. 残課題 (current backlog)

| # | 残 | 関連 | 状態 |
|---|---|---|---|
| 1 | M-Wave9 独自ドメイン + HTTPS + DNS (Web 公開基盤) — **Step 1〜6** ([§2 Wave 9](#wave-9--web-公開基盤-独自ドメイン--https--dns)) | §2 Wave 9 | ⏸ ドメイン購入タイミングで着手 |
| 2 | M-Wave8.7 ES production 化 (HTTPS + password auth) — **Step 7-1〜7-5** ([§2 Wave 8.7](#wave-87--es-production-化-https--password-auth)) | §2 Wave 8.7 | ⏸ Wave 9 完了後 (cert + DNS 先) |

実施順は **Wave 9 → Wave 8.7** (cert + DNS が外側、ES auth が内側 — 外側を先に揃えてから内側の認可強化)。両 Wave の具体手順 (gcloud / kubectl / file edit / 検証コマンド) は §2 にステップ展開済。

完了済 Wave (0/1/2/3/4/5/6/7/8 / M-Pivot / M-RunbookLocal / M-Wave8.5 / M-Wave8.6 Phase 1-3 + 後段 caller migration / Step.precondition framework / C4 Makefile python -u / PMLE doc / GCP ID rename `phase7-*` → `mlops-*` / `destroy-coast-down`) は [03_実装カタログ §7.3](../architecture/03_実装カタログ.md) を正本。

---

## §2. 残 Wave 詳細

### Wave 9 — Web 公開基盤 (独自ドメイン + HTTPS + DNS)

**目的**: Web アプリを GCP 上で独自ドメイン配信、HTTPS/TLS + DNS を canonical 手順で固定。Wave 9 完了後に Wave 8.7 (ES auth production 化) を続けて実施する (cert + DNS が先、internal auth は後)。

**前提**:
- M-Wave5 (継続改善サイクル) PASS 済 (canonical 経路が deployed cluster で動作)
- `make verify-live-acceptance` が green (Gateway 外部 IP 取得可能、`make ops-api-url` で確認)
- Billing 有効。Cloud Domains は前払い、`.com` で ~$12/yr

#### Step 1 — Cloud Domains で購入

GCP Console → Network services → Cloud Domains で `<your-domain>` を購入 (~$12/yr)。
購入時の auto-DNS-zone option は **無効化** (canonical な Terraform 配下に zone を置くため)。

```bash
gcloud domains registrations list --location=global --project=$PROJECT_ID
```

#### Step 2 — Cloud DNS Public Zone 作成 + NS 委任

```bash
gcloud dns managed-zones create mlops-public \
  --description="Public zone for $DOMAIN" \
  --dns-name="$DOMAIN." \
  --visibility=public \
  --project=$PROJECT_ID

gcloud dns managed-zones describe mlops-public \
  --project=$PROJECT_ID --format='value(nameServers)'
```

Cloud Domains 側で NS を上記 4 本に書き換え (購入時の Cloud DNS auto-zone を使わない設計)。
反映確認:

```bash
dig NS $DOMAIN +short    # 4 NS が GCP DNS を指していること
```

#### Step 3 — Gateway listener + HTTPRoute に独自ドメイン host 追加

`infra/manifests/search-api/gateway.yaml` の `spec.listeners[]` に HTTPS listener (`port: 443`, `protocol: HTTPS`, `tls.mode: Terminate`, `tls.options.networking.gke.io/pre-shared-certs: <cert-name>`) を追加。
`infra/manifests/search-api/httproute.yaml` の `spec.hostnames: ["$DOMAIN"]` に独自ドメインを追加 (既存 `search-api.example.com` 学習用 host と並列で残す形でも可)。

```bash
make apply-manifests
kubectl get gateway search-api-gateway -n search -o yaml | grep -A5 listeners
```

#### Step 4 — Google-managed certificate 作成 + Gateway バインド

```bash
gcloud compute ssl-certificates create mlops-search-cert \
  --domains="$DOMAIN" --global \
  --project=$PROJECT_ID

gcloud compute ssl-certificates describe mlops-search-cert \
  --global --project=$PROJECT_ID --format='value(managed.status)'
# ACTIVE になるまで待つ (DNS A record 完成 + プロビジョニング ~10-30 min)
```

Gateway の listener annotation `networking.gke.io/pre-shared-certs: mlops-search-cert` で binding。

#### Step 5 — A / AAAA を Gateway 外部 IP へ

```bash
GATEWAY_IP=$(make ops-api-url | sed 's|https://||')
gcloud dns record-sets create "$DOMAIN." \
  --zone=mlops-public --type=A --ttl=300 \
  --rrdatas="$GATEWAY_IP" --project=$PROJECT_ID
```

`AAAA` は Gateway IPv6 が必要な場合のみ。`CNAME` は apex には張れない (subdomain 用途のみ)。
反映確認:

```bash
dig +short $DOMAIN
```

#### Step 6 — smoke 疎通検証

```bash
curl -I "https://$DOMAIN"                              # 200 OK + cert chain
openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" </dev/null \
  | openssl x509 -noout -issuer -dates                  # Google Trust Services
API_URL="https://$DOMAIN" API_REQUIRE_TOKEN=false make ops-search
```

**完了条件**: 独自ドメイン経由で `/api/v1/search` が HTTPS 200 を返し、証明書が自動更新 (`managed.status=ACTIVE`)。**scope outside** (user 指示で除外継続、ドメイン購入タイミングで着手)。

---

### Wave 8.7 — ES production 化 (HTTPS + password auth)

**目的**: 学習用 (a') 解 (HTTP + anonymous superuser) を production grade へ移行。**Wave 9 完了後に着手** (Gateway HTTPS が外側、ES auth が内側 — 内側の認可強化は外側 cert 完成後でないと差分検証が混ざる)。

#### Step 7-1 — canonical URL の http/https 切替

```bash
# `scripts/ops/sync_elasticsearch.py`
#   --es-url default を https://elasticsearch.search.svc.cluster.local:9200 に
# `infra/manifests/search-api/configmap.yaml`
#   ELASTICSEARCH_URL を環境変数 ELASTIC_URL_SCHEME=https/http で切替可能に
```

#### Step 7-2 — ECK secret 経由 password fetch

ECK が `<cluster-name>-es-elastic-user` という Secret に `elastic` ユーザの初期 password を auto-generate する。`scripts/ops/sync_elasticsearch.py::_run_sync_elasticsearch` 冒頭で:

```python
auth_secret = kubectl_run(
    "get", "secret", "elasticsearch-es-elastic-user",
    f"--namespace={ES_NAMESPACE}",
    "-o", "jsonpath={.data.elastic}",
    capture=True,
)
import base64
es_password = base64.b64decode(auth_secret.stdout).decode()
```

これを httpx の `auth=("elastic", es_password)` に渡す。CI / search-api 側は ExternalSecret + KSA 経由で同 Secret を Pod 内に mount。

#### Step 7-3 — `xpack.security.authc.anonymous.*` 削除

```bash
# infra/manifests/elasticsearch/elasticsearch.yaml
#   spec.config から xpack.security.authc.anonymous.{username,roles,authz_exception} を削除
#   spec.http.tls.selfSignedCertificate.disabled: true も削除 (= ECK default の HTTPS+self-signed cert に戻る)
```

#### Step 7-4 — contract test を HTTPS+auth pin に更新

```bash
# tests/integration/parity/test_codebase_invariants.py::test_es_manifest_pins_http_and_anonymous_auth
#   anonymous.* token が manifest に **無い** ことを assert (現行の「ある」から反転)
```

#### Step 7-5 — CLAUDE.md / README で学習用 anonymous の禁忌を明記

「(a') 解の HTTP + anonymous superuser は学習プロジェクト前提。production では `xpack.security.authc.anonymous.*` を絶対に有効化しない」を追記。

**完了条件**: ES が ECK default の HTTPS+auth で動作、`make verify-live-acceptance` PASS、`test_es_manifest_pins_http_and_anonymous_auth` が新 pin で green。

---

## §3. 不変ルール / 非負制約

### §3.1 ⛔ ゴール劣化禁止

「本線」「必須」「canonical」「不変」と書かれた要件 (中核 5 要素 / Composer = 上位 orchestrator / 本線 retrain DAG / Feature View 経由 fetch / LightGBM 接続死守ライン) を **未達のまま「完了」「OK」と扱うのは禁止**。

禁止する hedging:
- 「深追いは別 sprint」「現状で X 完了とみなし次へ」「Stage X.Y 未解決のまま完了扱い」
- 「task SUCCEEDED は別 sprint」「live verify は別 session」「明日以降」「後追い」
- 判断 A/B が並列に書かれている場合、勝手に A を選んで B を別 sprint へ送る (User 明示確認なし)

正しい扱い:
1. 未達は ⚠️ マーカー付きで「**canonical 未達 (= ゴール劣化)、追加 sprint 必須**」と明示
2. 必須項目と機能影響低の項目を **明確に区別**
3. 違反が生じる選択肢は ~~取り消し線~~ で不採用宣言

### §3.2 中核 5 要素

**Elasticsearch BM25 + multilingual-e5 + Vertex AI Vector Search + RRF + LightGBM LambdaRank**。削除・置換・無効化は明示的な user 合意がない限り実施しない。

### §3.3 LightGBM 接続死守ライン

`pipeline/training_job/main.py` から `ml/data/loaders/ranker_repository.py` (BigQuery loader) を呼ぶ配線を維持、synthetic-only 学習へ退行禁止。

### §3.4 Composer × Vertex Pipelines 上下関係

Composer = 上位 orchestrator、Vertex Pipelines = 下位 ML executor。`train/evaluate/register` を Composer 側に書かない (カニバリ禁止)。Vertex `PipelineJobSchedule` は併存禁止。Cloud Scheduler / Eventarc / Cloud Function は smoke / manual のみ。

### §3.5 incident postmortem は contract test 化

過去 incident は `tests/integration/workflow/` の contract test として固定化済 (15 件以上)。新 incident も同パターンで固定化。詳細: [03_実装カタログ §7.4](../architecture/03_実装カタログ.md)。

---

## §4. リスクと回避

| リスク | 回避 |
|---|---|
| Wave の並行実施で API 境界が複数版混在 | Wave 1 (API 4 軸) 完了済 |
| LightGBM 接続死守ラインを「Wave 5 で代替」と勘違いし飛ばす | §3.3 死守ライン明記 |
| ES 移行で同義語辞書 (`SynonymExpanderPort`) を破壊 | Redis 経路は維持、adapter 差し替えのみ |
| Wave 7 (Makefile 整理) を Wave 1-6 と同時に走らせる | Wave 1-6 完了後に着手 (前提達成済) |
| deployed_index 残置による VVS 課金事故 (1 replica = ¥1,460/日) | `make destroy-all` で能動 undeploy + Cloud Scheduler 自動 undeploy (backlog) + Billing Budget Alert (backlog) |

### §4.9 VVS 永続化 lessons learned

2026-05-03 incident で `Instance cannot be destroyed` が発生し `prevent_destroy` 設計が teardown と衝突。以後は **`prevent_destroy` 不採用、state rm + GCP 残置 pattern** を採用。

- `destroy-all` で永続化したい VVS リソースは `state rm` で tfstate から外す
- 次回 `deploy-all` では `terraform import` で state 復帰
- `state-recover` runbook と対で扱う

将来 backlog: Stack 分離、Cloud Scheduler 自動 undeploy、Billing Alert、health check 強化。

---

## §5. 残マイルストーン

| ID | 内容 | 状態 |
|---|---|---|
| M-Wave8.7 | ES production 化 (HTTPS + password) | ⏸ ドメイン購入後 (M-Wave9 と同時推奨) |
| M-Wave9 | 独自ドメイン + HTTPS + DNS | ⏸ scope outside |

完了済は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §7.3 を正本。

---

## §6. 関連ドキュメント

- [`TASKS.md`](TASKS.md) — current sprint
- [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) — canonical 仕様
- [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) — 実装スナップショット + マイルストーン履歴 + incident memo
- [`../runbook/04_検証.md`](../runbook/04_検証.md) / [`../runbook/05_運用.md`](../runbook/05_運用.md) — 検証 / PDCA
- [`../decisions/README.md`](../decisions/README.md) — ADR 0001〜0008
- [`../troubleshooting/`](../troubleshooting/) — incident memo (eck-license-reconcile-stall / terraform-lock-stale-after-bg-kill / bg-pipe-fake-exit-zero)
- [`../pmle-learning-notes.md`](../pmle-learning-notes.md) — PMLE 学習 doc (試験対策、本リポ実体験起点)
- [`../conventions/`](../conventions/) — 命名 / 配置 / Make / Docker 規約
