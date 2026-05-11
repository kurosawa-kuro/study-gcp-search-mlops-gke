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

### §0.4 公開ドメイン (M-Wave9、2026-05-11 購入)

- ドメイン: **`gcp-search-mlops-gke.dev`** (Cloud Domains で購入。`.dev` TLD = Google が運用、**HSTS preload 強制 → HTTPS 必須** — HTTP-only でブラウザ到達不可、`curl` は HTTP でも可)
- Cloud DNS public zone: **`gcp-search-mlops-gke-dev`** (DNS 名 `gcp-search-mlops-gke.dev.`、DNSSEC on、ゾーンタイプ 公開)。**console で手動作成済** — Terraform 側は `data "google_dns_managed_zone"` で参照 (zone 自体は import せず管理外、record-set のみ Terraform 管理)
- GKE Gateway TLS は **Certificate Manager** 経由 (DNS-01 authorization + certmap annotation)。旧 self-signed Secret (`kserve/tls_dev.tf`) は `enable_self_signed_tls=false` で無効化、`api_insecure_tls` も解除

---

## §1. 残課題 (current backlog)

| # | 残 | 関連 | 状態 |
|---|---|---|---|
| 1 | M-Wave9 独自ドメイン + HTTPS + DNS (Web 公開基盤) — Step 1-2 (購入 / DNS zone) + Step 3-5 (コード: `module.dns` / gateway certmap+static IP / `_common.resolve_api_target` 公開ドメイン化 / var 配線) **完了 2026-05-11**。残り Step 6 (deploy → `curl -I https://gcp-search-mlops-gke.dev` smoke、cert ACTIVE 確認) のみ ([§2 Wave 9](#wave-9--web-公開基盤-独自ドメイン--https--dns)) | §2 Wave 9 | 🔨 deploy 待ち |
| 2 | M-Wave8.7 ES production 化 (HTTPS + password auth) — **Step 7-1〜7-5** ([§2 Wave 8.7](#wave-87--es-production-化-https--password-auth)) | §2 Wave 8.7 | ⏸ Wave 9 完了後 (cert + DNS 先) |

実施順は **Wave 9 → Wave 8.7** (cert + DNS が外側、ES auth が内側 — 外側を先に揃えてから内側の認可強化)。両 Wave の具体手順 (gcloud / kubectl / file edit / 検証コマンド) は §2 にステップ展開済。

完了済 Wave (0/1/2/3/4/5/6/7/8 / M-Pivot / M-RunbookLocal / M-Wave8.5 / M-Wave8.6 Phase 1-3 + 後段 caller migration + adapter 移行漏れ後処理 / Step.precondition framework / C4 Makefile python -u / PMLE doc / GCP ID rename `phase7-*` → `mlops-*` / `destroy-coast-down` / EventWriter Pub/Sub 統一 / M-Wave9 Step 1-5 公開ドメイン) は [03_実装カタログ §7.3](../architecture/03_実装カタログ.md) を正本。

---

## §2. 残 Wave 詳細

### Wave 9 — Web 公開基盤 (独自ドメイン + HTTPS + DNS)

**目的**: Web アプリを GCP 上で独自ドメイン配信、HTTPS/TLS + DNS を canonical 手順で固定。Wave 9 完了後に Wave 8.7 (ES auth production 化) を続けて実施する (cert + DNS が先、internal auth は後)。

**ドメイン (確定値)**: `gcp-search-mlops-gke.dev` / Cloud DNS public zone `gcp-search-mlops-gke-dev` ([§0.4](#04-公開ドメイン-m-wave92026-05-11-購入) 参照)。

**前提**:
- M-Wave5 (継続改善サイクル) PASS 済 (canonical 経路が deployed cluster で動作)
- Billing 有効

#### Step 1 — Cloud Domains で購入 ✅ 完了 (2026-05-11)

`gcp-search-mlops-gke.dev` を購入済。確認: `gcloud domains registrations list --location=global --project=$PROJECT_ID`

#### Step 2 — Cloud DNS Public Zone 作成 ✅ 完了 (2026-05-11、console で手動作成)

Zone `gcp-search-mlops-gke-dev` (DNS 名 `gcp-search-mlops-gke.dev.`、public、DNSSEC on)。`.dev` は Cloud Domains 購入時に Google 側で NS 委任が自動完了するため別途 NS 書換え不要。Terraform 側は `data "google_dns_managed_zone"` で参照し、record-set のみ管理 (zone は import せず管理外)。確認: `dig NS gcp-search-mlops-gke.dev +short`

#### Step 3 — Gateway: 静的 IP + certmap annotation + hostname 差替え ✅ コード完了 (2026-05-11)

`infra/manifests/search-api/gateway.yaml`:
- `spec.addresses: [{type: NamedAddress, value: search-api-ip}]` — `module.dns` の `google_compute_global_address` を pin (ephemeral IP → A record の chicken-and-egg を回避)
- annotation `networking.gke.io/certmap: search-api-certmap` — Certificate Manager の certmap を bind (実 TLS はこれ)
- listener `hostname` / HTTPRoute `hostnames` を `gcp-search-mlops-gke.dev` に
- listener の `tls.certificateRefs: [Secret search-api-tls]` (self-signed) は **placeholder として残す** — certmap がある時 controller が無視するが、listener が PROGRAMMED になるために必要。`module.kserve` が CN=`var.public_domain` で生成 (`enable_self_signed_tls=true` のまま、`tls_cn=var.public_domain`)

確認: `kubectl get gateway search-api-gateway -n search -o yaml`

#### Step 4 — Certificate Manager (DNS-01 authorization) ✅ コード完了 (2026-05-11)

新 module `infra/terraform/modules/dns/` で:
- `google_certificate_manager_dns_authorization` (`location="global"`) — `gcp-search-mlops-gke.dev` の DNS-01 authorization (LB IP に依存せず発行可能)
- `google_dns_record_set` (CNAME) — dns_authorization が要求する検証レコード (`dns_authorization.dns_resource_record[0].{name,type,data}` を流し込む)
- `google_certificate_manager_certificate` (managed、`location="global"`) — 上の dns_authorization を参照
- `google_certificate_manager_certificate_map` + `google_certificate_manager_certificate_map_entry` — hostname `gcp-search-mlops-gke.dev` → cert

GKE Gateway は `networking.gke.io/certmap: <map-name>` annotation で certmap を消費する (classic `google_compute_managed_ssl_certificate` + `pre-shared-certs` は Ingress 用で Gateway API では使えない)。`dns.googleapis.com` を apis.tf に追加 (certificatemanager / networkservices は既存)。

確認 (deploy 後): `gcloud certificate-manager certificates describe search-api-cert --project=$PROJECT_ID --format='value(managed.state)'` が `ACTIVE` になるまで待つ (DNS-01 検証 ~数分〜30 min)

#### Step 5 — A レコードを静的 IP へ ✅ コード完了 (2026-05-11)

`infra/terraform/modules/dns/` の `google_dns_record_set` (A) — `gcp-search-mlops-gke.dev.` → `google_compute_global_address.search_api.address`。静的 IP なので Terraform plan 時点で値が確定 (Gateway 起動を待たない)。`AAAA` は IPv6 が要る場合のみ。apex に `CNAME` は張れない。`module.dns` は `dev/main.tf` で配線、`dev/outputs.tf` に `public_domain` / `gateway_ip_name` / `gateway_ip_address` / `certificate_map_name` / `certificate_name` を expose。

確認 (deploy 後): `dig +short gcp-search-mlops-gke.dev`

**Step 3-5 のコード一式 (2026-05-11)**: `env/config/setting.yaml` に `public_domain` / `dns_zone_name` 追加 → Makefile が `-var=public_domain=...` `-var=dns_zone_name=...` を流す (`_common.terraform_var_args()` を canonical な `CANONICAL_TF_VAR_NAMES` 既定にリファクタ、`tf_apply` / `destroy_all` / `recover_wif` / `state_recovery` の caller を `()` 呼びに統一)。`scripts/_common.py::resolve_api_target()` の `TARGET=gcp` を「`PUBLIC_DOMAIN` あり → `https://<domain>` + `verify_tls=True` / なし → Gateway IP fallback」に二段化。`composer/main.tf` の `API_HOST_HEADER` / `API_INSECURE_TLS` 注入と `pipeline/dags/_pod.py` の hardcoded default を撤去 (正規 cert なので不要)。`make check` 818 passed / 2 skipped、`make tf-validate` / `tf-fmt` PASS。新 contract test: `test_public_domain_consistency.py` (gateway.yaml hostname == setting.yaml::public_domain / certmap annotation 存在 / static IP pin / `module.dns` 配線) + `test_resolve_api_target.py` の `TARGET=gcp` セクション書換え。

#### Step 6 — smoke 疎通検証 (deploy 後、runtime)

```bash
curl -I https://gcp-search-mlops-gke.dev                 # 200 + Google Trust Services cert
openssl s_client -connect gcp-search-mlops-gke.dev:443 -servername gcp-search-mlops-gke.dev </dev/null \
  | openssl x509 -noout -issuer -dates
API_URL=https://gcp-search-mlops-gke.dev API_REQUIRE_TOKEN=false make ops-search
```

`_common.py` の `resolve_api_target()` は `TARGET=gcp` 時 `gateway_url()` (= `kubectl get gateway` の external IP) を返すが、Wave 9 後は **静的 IP + 正規 cert + 正規 hostname** になるため `DEFAULT_GATEWAY_HOST_HEADER` を `gcp-search-mlops-gke.dev` に、`verify_tls` を `True` に切替える (self-signed 時代の Host ヘッダ偽装 + TLS 検証スキップが不要に)。

**完了条件**: `https://gcp-search-mlops-gke.dev/api/v1/search` が HTTPS 200、`certificate_manager` の `managed.state=ACTIVE` で自動更新、`make ops-search` が `TARGET=gcp` (= 正規ドメイン) で通る。

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
| M-Wave9 | 独自ドメイン + HTTPS + DNS — Step 1-5 (購入 / DNS zone / `module.dns` / gateway certmap+static IP / var 配線 + `resolve_api_target` 公開ドメイン化) **完了 2026-05-11**。残り Step 6 (deploy → smoke、cert ACTIVE 確認) のみ | 🔨 deploy 待ち |
| M-Wave8.7 | ES production 化 (HTTPS + password auth) | ⏸ M-Wave9 完了後 |
| `infra/` Phase 残骸 scrub | Terraform module + manifest のコメント ~25 箇所 (M-Wave8.5 が docs/ + tests/ のみだった分)。コード影響なし | ⏳ 着手可 |

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
