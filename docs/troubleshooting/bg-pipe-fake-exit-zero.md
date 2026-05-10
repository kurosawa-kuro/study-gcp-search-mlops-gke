# bg `make ... 2>&1 | tail -100` の偽 exit 0 罠

## 症状

Claude Code から bg bash で `make foo 2>&1 | tail -100` を実行 → 完了通知に `exit code 0` が表示される → 実は内部で fail している。

実例 (2026-05-10 incident):

```bash
uv run python -m scripts.setup.deploy_all --from-step sync-elasticsearch --to-step sync-elasticsearch 2>&1 | tail -25
```

通知: `Background command "..." completed (exit code 0)`

実際の output:

```
httpx.RemoteProtocolError: Server disconnected without sending a response.
==> deploy-all FAILED at step 10 (sync-elasticsearch) — see traceback above
```

= 内部 Python は exit 1 で死んだが、**`tail` 自身は標準入力を読めて正常終了 = exit 0**。bash の終了 code はパイプライン末尾コマンドの code = `tail` の 0。

## 根本原因

POSIX shell のデフォルトは「パイプライン全体の exit code = 末尾コマンドの code」。中間コマンドの fail は黙殺される。

## 対処

### 1. `pipefail` を使う

```bash
set -o pipefail
make foo 2>&1 | tail -100
echo $?  # ← 中間 fail が伝播
```

bash の場合 1 行で:

```bash
bash -c 'set -o pipefail; make foo 2>&1 | tail -100'
```

### 2. 中間出力を `tee` で保存して exit code を別取得

```bash
make foo 2>&1 | tee /tmp/foo.log
status=${PIPESTATUS[0]}
[ "$status" -eq 0 ] || echo "FAILED ($status), see /tmp/foo.log"
```

### 3. tail パイプを使わない (走行中の visibility 問題も同時に解消)

```bash
make foo > /tmp/foo.log 2>&1 &
tail -f /tmp/foo.log  # 別ターミナル / 別 bg job で進捗監視
```

bg job が完了したら `/tmp/foo.log` 全体を `tail -<n>` で確認。`make` の真の exit code は wait で取れる:

```bash
make foo > /tmp/foo.log 2>&1 &
pid=$!
wait $pid
echo "exit=$?"
```

### 4. Bash tool 経由の場合

Bash tool は `command 2>&1 | tail -<n>` を `run_in_background: true` で実行することが多いが、**通知の exit code は信用できない**ことを覚えておく。

完了通知後は **必ず output ファイル末尾を読んで `FAILED` / `Error:` / `Traceback` を grep** する:

```bash
tail -30 /tmp/.../bg-output.txt | grep -E "FAILED|Error:|Traceback|exit code [^0]"
```

これで偽 exit 0 を検出できる。

## 推奨パターン (Claude Code 内)

bg make / python 実行時は:

```bash
make foo 2>&1 | tee /tmp/foo.log; exit ${PIPESTATUS[0]}
```

または bash 関数として:

```bash
bash -c 'set -o pipefail; make foo 2>&1 | tail -100'
```

これで pipefail 経由で真の exit code が伝播する。

## 過去事故

| 日付 | 事象 | 失われた時間 |
|---|---|---|
| 2026-05-10 | step 10 sync-elasticsearch の偽 exit 0 を 3 回見落とし、ECK reconcile stall の root cause 把握まで遅延 | ~30 分 |

## 関連

- bg job visibility 問題 (output 0 byte): 上記 §3 の `tee` + `tail -f` パターンで同時解消
- 反省を test 化: 各 step の真の exit code は `_run_*` の戻り値 ≠ 0 を `main()` ループで `print(...FAILED at step ...)` するよう pin (`scripts/setup/deploy_all.py` / `scripts/setup/destroy_all.py`)
