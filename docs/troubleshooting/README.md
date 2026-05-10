# Troubleshooting index

過去 incident の症状 → 判断 → 推奨手順をまとめた hub。新 incident は同じ format で追加し、再発時の判断材料を残す。

## Cluster / Infra

| Doc | 症状 | 判断 |
|---|---|---|
| [eck-license-reconcile-stall.md](eck-license-reconcile-stall.md) | ECK の `Phase=ApplyingChanges Health=unknown` が N 時間継続、HTTP API 無応答 | log 調査より destroy-all 優先 (sunk cost cut) |
| [terraform-lock-stale-after-bg-kill.md](terraform-lock-stale-after-bg-kill.md) | bg kill 後 terraform 操作が `Error 412 conditionNotMet` で fail | `TERRAFORM_STATE_FORCE_UNLOCK=1` で自動回復、parser fail 時は手動 `force-unlock` |

## Workflow / Tooling

| Doc | 症状 | 判断 |
|---|---|---|
| [bg-pipe-fake-exit-zero.md](bg-pipe-fake-exit-zero.md) | bg `make ... 2>&1 \| tail -N` の完了通知が exit 0 だが内部で fail | `pipefail` / `tee + ${PIPESTATUS[0]}` パターン使用、完了通知後は output 末尾を grep で確認 |

---

## 一般則 (これらの incident に共通する判断軸)

### 1. 「技術的に正しい解より時間軸で正しい解」
ML pipeline / infra reconciler の stall 系は、**debug の expected value > clean rebuild の expected value** が成立するかを最初に判定。reconcile が N 時間ストールしている時点で前者は負け筋になりやすい。

### 2. 「再現性が確認できるまでは debug より destroy」
state 汚染由来かもしれない症状を、同じ state のまま小手先で直すと再発する。clean state での再現を最初に確認すべき。

### 3. 「sunk cost に引きずられない」
既に N 時間 cluster live でコスト累積していても、それは sunk cost。**追加で累積させないこと** が最大の節約軸。

### 4. 「偽 exit 0 / 偽 PASS を疑う」
- Pipe の末尾コマンドの exit code は中間 fail を黙殺する
- Test の literal が **本物の escape sequence** か **見た目の文字列** かで実 PASS / 偽 PASS が分かれる
- `bg notification` の exit 0 は信用するな、output 末尾を必ず grep

### 5. 「reconcile / wait 系は明示的 timeout で fail-fast」
ECK の Phase 遷移、terraform plan/apply、kubectl wait など **外部 reconciler の完了待ち** は、**読める timeout を必ず設定**する。default の無限待ちは「異常を異常として観測する」道を塞ぐ。

---

## 新 incident を追加する時の format

```markdown
# <incident 名>

## 症状

<ログ抜粋 / 状態スナップショット>

## 判断

<選んだ対処と理由 (alternatives と expected value 比較)>

## 推奨手順

<step-by-step>

## 過去事故

| 日付 | 事象 | 教訓 |

## 関連

<sibling docs / 設計判断 / contract test>
```

追加後は本 README index にも 1 行追記。
