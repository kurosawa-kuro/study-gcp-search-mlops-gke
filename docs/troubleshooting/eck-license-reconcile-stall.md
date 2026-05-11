# ECK license reconcile stall

## 症状

ECK (Elastic Cloud on Kubernetes) で `Elasticsearch` CR が以下の状態で長時間ストールする:

```
HEALTH    NODES   VERSION   PHASE             AGE
unknown   1       8.13.4    ApplyingChanges   <数時間〜数十時間>
```

`kubectl describe elasticsearch <name> -n <ns>` で:

- `ReconciliationComplete: False`
  Message: `Could not reconcile cluster license, re-queuing`
- `ElasticsearchIsReachable: False`
  Message: `Service <ns>/<svc>-es-internal-http has endpoints but Elasticsearch is unavailable`
- `Phase: ApplyingChanges`
- `Health: unknown`

ES pod 自体は `Running 1/1` で、log では cluster.health = GREEN を確認できることがある (= ES 本体は起動してデータも load されているが、ECK Operator 側の reconciliation がストールしている)。

`scripts/ops/sync_elasticsearch.py` などで HTTP API を叩くと:

```
httpx.RemoteProtocolError: Server disconnected without sending a response.
```

= TLS handshake or auth で切断される。ECK が Service / Secret の更新を完了できていないので外部から到達できない。

## 判断

**log 調査より destroy-all 優先** (sunk cost cut)。

理由 (2026-05-10 incident で確定):

1. `Could not reconcile cluster license` が N 時間続いている時点で、operator log を読んでも「license controller が API server に到達できない」「trial license の再発行に失敗」など、その場での修正コストが destroy-all (5-7 分) を上回る系統のエラーである確率が高い。
2. cluster は **コスト累積中** = これ以上累積させないことが最優先。
3. ECK reconcile stall は **state 汚染由来** であることが多く、同じ state のまま pod 再作成しても再発する確率が無視できない。clean state からの deploy-all の方が、デバッグ可能性も含めて健全。

## 推奨手順

### 1. (今回は skip) ECK Operator log を一応取ってから destroy

再発時の判断材料を残すため、destroy する前に operator log を取る:

```bash
kubectl logs -n elastic-system $(kubectl get pods -n elastic-system -l control-plane=elastic-operator -o name | head -1) \
  --tail=500 > /tmp/eck-operator.log
```

時間に余裕がない場合は skip して直接 destroy-all。

### 2. destroy-all で全消し

```bash
make destroy-all
```

新 step 分離後 (`docs/architecture/03_実装カタログ.md §7.3 M-Wave8.6 教育用フェーズ初期`) は 8 step を順次実行。`--from-step` / `--to-step` で 段階的にも可能。

### 3. cost stop 確認

```bash
kubectl get nodes  # → NotFound or 0 nodes
gcloud composer environments list --locations=asia-northeast1  # → 空
```

`destroy-all` 後は `tfstate bucket` と `API 有効化` のみ残置 (永続化 VVS Index/Endpoint は `state rm + GCP 残置` 設計、`docs/tasks/TASKS_ROADMAP.md §4.9`)。

### 4. 翌回 deploy-all 前に ECK manifest を確認

`infra/manifests/elasticsearch/` 配下の ECK manifest と `infra/terraform/modules/elasticsearch/` の version pin を確認:

- ECK Operator version (`elastic-operator` Helm chart の `appVersion`)
- Elasticsearch CR の `spec.version`

最後に動作確認できた version との差分があれば pin を戻す。

## 破綻条件

| 条件 | 対処 |
|---|---|
| 翌回 deploy-all で **同じ ECK reconcile stall が再発** | state 汚染ではなく ECK version or manifest 側の bug。その時点で初めて operator log 調査に価値が出る (再現性が確認できているので調査対象が絞れる) |
| `destroy-all` 自体が ES finalizer で stuck | `kubectl patch elasticsearch <name> -n <ns> -p '{"metadata":{"finalizers":[]}}' --type=merge` で finalizer 強制除去 |

## 一般化

**「MLOps における障害判断は、技術的に正しい解より時間軸で正しい解」**。

ML pipeline の reconcile stall 系一般に転用できる思考:
- 短期 (1-2 sprint): debug log + 修正の expected value vs clean rebuild の expected value を比較
- 累積コストの sunk cost cut が遅延すると、debug の learning は得られても session 全体は負け筋
- **再現性が確認できるまでは debug より destroy** が筋

## 関連

- 設計判断: `docs/tasks/TASKS_ROADMAP.md §3.1` (ゴール劣化禁止) / §4.9 (VVS 永続化 lessons learned)
- destroy-all step 分離: `docs/architecture/03_実装カタログ.md §7.3` M-Wave8.6 教育用フェーズ初期
- 過去の類似 cost-cut 判断: `docs/tasks/TASKS_ROADMAP.md §4.10` (state recovery 12 type 拡張)

---

## 2026-05-10 真の root cause 確定 (本 doc 旧版の判断指針通り、2 回連続再発で初めて見えた)

### 表層症状
`Phase=ApplyingChanges Health=unknown` が永続化、HTTP API 無応答。

### 本質原因 (2 つの構造的 bug の重ね合わせ)

#### Bug 1: NetworkPolicy が ECK Operator namespace を block

`infra/manifests/elasticsearch/networkpolicy.yaml` の ingress に **`elastic-system` ns 漏れ**:

```yaml
# 修正前
ingress:
  - from:
    - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: search } }
    - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kserve-inference } }
    # ↑ elastic-system が抜けている
    ports: [{ protocol: TCP, port: 9200 }]
```

ECK Operator は `https://<es>:9200/_security/api_key?name=eck-*` を呼んで reconcile する。block されると `dial tcp: connect: connection timed out` で `Phase=ApplyingChanges` 永続化。

#### Bug 2: canonical URL `http://...` と ECK 8.x default `xpack.security.http.ssl.enabled=true` の不整合

ECK 8.x は default で HTTPS only + auth 必須。`http://elasticsearch.search.svc.cluster.local:9200` で接続すると、TLS expected で plain HTTP が来る → handshake fail → **`Server disconnected without sending a response`**。

Bug 1 は ECK Operator 側、Bug 2 は client 側 (`sync_elasticsearch.py` 経由)。両方直さないと完走しない。

### 採用解決策 (a' = 学習プロジェクト前提)

1. **NetworkPolicy 修正**: `elastic-system` ns ingress を ingress 許可に追加
2. **ES manifest 修正**:
   - `spec.http.tls.selfSignedCertificate.disabled: true` で TLS 無効化 (canonical URL `http://...` 維持)
   - `spec.nodeSets[].config.xpack.security.authc.anonymous.username/roles/authz_exception` で **anonymous superuser** auth bypass。security stack は ON のまま (ECK 8.x の deprecated path 回避)

これで:
- canonical URL `http://elasticsearch.search.svc.cluster.local:9200` のまま
- Wave 8 contract test 無修正
- ES `health=green` + HTTP 200 (anonymous accepted) で sync 通過

### production 化の手順 → [`docs/backlog/production-hardening.md`](../backlog/production-hardening.md) に保管 (active backlog からは外し parked、2026-05-11)

学習リポジトリは production hardening を追わない判断。手順 (canonical URL の http/https 切替 / ECK `elasticsearch-es-elastic-user` secret から password fetch / `xpack.security.authc.anonymous.*` 削除 / contract test 反転 / docs 注記) + 判断記録 + 破綻条件は上記ファイルを正本。学習用 anonymous superuser が **production 厳禁** である旨は CLAUDE.md / README に明示済 (contract test `test_es_manifest_pins_http_and_anonymous_auth` が現行 pin として自己拘束)。

### 教訓

- 「2 回連続発症で初めて log 調査の価値が出る」判断指針は機能した = **再現性確認 → 調査 → root cause 特定 → 修正 → 1 分で復旧**
- 前日 (5/9) の destroy-all 判断は **時間効率としては正解**、ただし root cause は state 汚染ではなく **manifest bug** だった
- `wait_until_es_healthy` の 5 min timeout は「観測窓」として機能した。前回は 14h 放置で何も観測できなかった
- **Manifest review 観点**: NetworkPolicy を書く時は **どの ns からの ingress が必要か** を operator / sidecar / probe / scrape 全部漏れなく列挙する。ECK は `elastic-system` ns から reconcile するので必須

### 関連 contract test (再発防止、2026-05-10 実装済)

`tests/integration/parity/test_codebase_invariants.py`:

- `test_es_networkpolicy_allows_eck_operator_namespace` ✅ — NetworkPolicy に `elastic-system` ns ingress を pin
- `test_es_manifest_pins_http_and_anonymous_auth` ✅ — HTTP + anonymous superuser の維持を pin、production 化境界判断点

### close 確定 (2026-05-10)

採用解 (a') の妥当性は **T1 PASS で実証**:

```
make verify-live-acceptance → PASSED (22.68s)
ops-search-components: lexical=4 / semantic=3 / rerank=5 all non-zero
readyz_rerank_enabled=True
model_path=property-reranker-predictor.kserve-inference.svc.cluster.local/v2/models/property-reranker/infer
```

= **HTTP + anonymous superuser が中核 5 要素を阻害しない** ことを実測。本 incident は **doc 化 + contract test 化 + production 化手順を `docs/backlog/production-hardening.md` に保管 (active backlog からは外し parked)** で完全 close。

### 「次の自分への手紙」

- **HTTP + anonymous は学習限定の意図的選択**。production 化する場合は HTTPS + password auth へ移行（手順: `docs/backlog/production-hardening.md`）。学習リポジトリでは追わない判断 (2026-05-11)
- **KServe cold start 由来の T1 timeout** = 初回 e2e は warm-up retry が必要。CI では `make ops-livez` 後に `sleep 30` を挟むのが安全。今回は 1 回目 timeout → 2 回目 22.68s で PASS
- **deploy-all resume 497s** が persistent stack 設計 (VVS Index/Endpoint 残置) の有効性実測値、次回比較ベースライン
