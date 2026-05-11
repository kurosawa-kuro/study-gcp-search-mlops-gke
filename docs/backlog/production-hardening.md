# Production hardening (parked — active backlog からは外す)

本リポジトリは **個人技術学習プロジェクト**（README §1 / CLAUDE.md「このリポジトリの性質」）であり、production posture の作り込みは**意図的に追わない**。ここはその「やる場合の手順」を保管する場所。`docs/tasks/TASKS_ROADMAP.md` §1 の active backlog には載せない。

---

## 判断記録: 学習リポジトリは production hardening を追わない (2026-05-11)

ES の production 化（旧 M-Wave8.7 / Wave 8.7）を active backlog から外し、本ファイルに parked する判断を確定した。

**理由**:
1. **目的と整合しない** — このリポの目的は「行動ログ → 正解データ → 再学習 → 評価 → deployment gate」の MLOps サイクル実装 + PMLE 学習 + 実務（商品検索）転用の検証。ES の認可設定は PMLE 範囲外で、実務転用時の差分は「検索品質 / 特徴量設計 / ランキング学習」側であり、production posture は実務側で別途設計すればよく学習リポで先取りする ROI が低い。
2. **「評価が運用に先行する」順序原則に反する** — 評価系（Vector Search 3 層永続化 / `ml/` 配下の再編 等）がまだ optimizing 中の段階で運用ポスチャ強化を入れるのは順序が逆。
3. **リスクが学習価値に見合わない** — 2026-05-10 の ECK reconcile stall を再現させるリスクがゼロでなく、live cluster の再 reconcile 待ちで 30-60min 消費、ExternalSecret + KSA + adapter 配線は「広く浅く」触る作業で MLOps の judgment density が高い領域ではない。同じ 2-3h を Vertex AI Feature Store / Vector Search の概念深掘り or PMLE ドリルに投下した方が優位。

**自己拘束**: contract test `tests/integration/parity/test_codebase_invariants.py::test_es_manifest_pins_http_and_anonymous_auth` は **現行 pin のまま残す**（= ES manifest に `selfSignedCertificate.disabled: true` と `xpack.security.authc.anonymous.username: anonymous_user` / `roles: superuser` が**ある**ことを assert）。これが「学習用途であることの明示的拘束」として機能する。production 化に踏み切る時はこの test を反転させること（= 反転が production 化のゲート）。

**この判断を再評価する破綻条件**（いずれか発生したら本ファイルを active backlog に戻す）:
1. このリポを外部公開して採用・営業の portfolio に使う方針に変える → production posture を見せる必要 → 下記 A（コード整備）
2. 商品検索（実務）に同じ ES クラスタを転用することが決まる → 下記 B（完全 production 化）
3. 同一 GKE クラスタに第三者ワークロードが乗る → superuser bypass が現実リスクに → B
4. PMLE 試験で ES 認可関連が範囲に含まれる（可能性低） → A（学習材料化）

着手時の選択肢: **A = コード変更（manifest / test / script / app）だけ入れて `make check` まで、deploy は別タイミング** / **B = deploy まで通して完全 production 化**。なお「コードを書いて deploy しない半端な状態」は次の `make deploy-all` で予期せず適用される or 適用されず差分が残るの両方のリスクがあるため、A を取るなら deploy 適用のタイミングを明示すること。

---

## ES production 化 — HTTPS + password auth（旧 Wave 8.7、Step 7-1〜7-5）

**現状（学習用 (a') 解）**: `infra/manifests/elasticsearch/elasticsearch.yaml` は `spec.http.tls.selfSignedCertificate.disabled: true`（ES を HTTP で listen）+ `xpack.security.authc.anonymous.{username=anonymous_user, roles=superuser, authz_exception=false}`（匿名 = superuser、= 実質 auth bypass）。canonical URL は `http://elasticsearch.search.svc.cluster.local:9200`（search-api ConfigMap の `ELASTICSEARCH_URL` / `scripts/ops/sync_elasticsearch.py --es-url`）。2026-05-10 の ECK reconcile stall（`http://...` の canonical URL と ECK 8.x default HTTPS の不整合 → `Server disconnected`）の最短収束策。

**目的**: 学習用 (a') 解を production grade（HTTPS + password auth）へ移行。実施するなら Gateway HTTPS（M-Wave9 で完了）が外側、ES auth が内側 — 外側 cert 完成後でないと差分検証が混ざる、という順序。

### Step 7-1 — canonical URL の http/https 切替

```bash
# `scripts/ops/sync_elasticsearch.py`
#   --es-url default を https://elasticsearch.search.svc.cluster.local:9200 に
# `infra/manifests/search-api/configmap.yaml`
#   ELASTICSEARCH_URL を環境変数 ELASTIC_URL_SCHEME=https/http で切替可能に
```

### Step 7-2 — ECK secret 経由 password fetch

ECK が `<cluster-name>-es-elastic-user`（= `elasticsearch-es-elastic-user`）という Secret に `elastic` ユーザの初期 password を auto-generate する。`scripts/ops/sync_elasticsearch.py::_run_sync_elasticsearch` 冒頭で:

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

### Step 7-3 — `xpack.security.authc.anonymous.*` 削除

```bash
# infra/manifests/elasticsearch/elasticsearch.yaml
#   spec.config から xpack.security.authc.anonymous.{username,roles,authz_exception} を削除
#   spec.http.tls.selfSignedCertificate.disabled: true も削除 (= ECK default の HTTPS+self-signed cert に戻る)
```

### Step 7-4 — contract test を HTTPS+auth pin に更新

```bash
# tests/integration/parity/test_codebase_invariants.py::test_es_manifest_pins_http_and_anonymous_auth
#   anonymous.* token が manifest に **無い** ことを assert (現行の「ある」から反転)
#   ※ この反転 = production 化に踏み切ったことの宣言。反転前に実装を完成させること。
```

### Step 7-5 — CLAUDE.md / README で学習用 anonymous の禁忌を明記（= 現行も既に記載済）

「(a') 解の HTTP + anonymous superuser は学習プロジェクト前提。production では `xpack.security.authc.anonymous.*` を絶対に有効化しない」。本リポでは parked 判断（2026-05-11）に合わせて CLAUDE.md / README.md に既にこの注記が入っている。production 化時はその注記を「production 化済」表現へ更新する。

**完了条件**（production 化を実施した場合）: ES が ECK default の HTTPS+auth で動作、`make verify-live-acceptance` PASS、`test_es_manifest_pins_http_and_anonymous_auth` が新 pin で green。
