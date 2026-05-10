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

新 step 分離後 (`docs/architecture/03_実装カタログ.md §7.3 M-Wave8.6 Phase 1`) は 8 step を順次実行。`--from-step` / `--to-step` で 段階的にも可能。

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
- destroy-all step 分離: `docs/architecture/03_実装カタログ.md §7.3` M-Wave8.6 Phase 1
- 過去の類似 cost-cut 判断: `docs/tasks/TASKS_ROADMAP.md §4.10` (state recovery 12 type 拡張)
