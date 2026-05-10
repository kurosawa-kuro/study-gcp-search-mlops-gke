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
| 2026-05-10 | **`tee` の block buffer で log file が 41 分間 flush せず、stage1 apply が stuck と誤判定しかけた**。実際は Composer creation 待ちで GCP 側は正常進行 | ~10 分 (誤診断と確認時間) |

## tee の block buffer 問題 (visibility ゼロ罠)

### 症状

```bash
make deploy-all 2>&1 | tee /tmp/deploy-all.log &
# 41 分後...
ls -la /tmp/deploy-all.log
# → mtime: 12:55 (41 分前)、サイズ更新なし
tail -30 /tmp/deploy-all.log
# → 41 分前と同じ末尾、何も追記されていない
```

しかし terraform プロセス自体は alive:

```bash
ps -o pid,etime,pcpu,wchan -p $(pgrep -f terraform)
# → ELAPSED 40:30、CPU 0.3%、WCHAN futex_wait_queue
cat /proc/$(pgrep -f terraform)/io
# → wchar: 21,835,950 (terraform は 21 MB stdout に書いた)
```

= terraform は 21 MB stdout に出力済、しかし tee → /tmp/log には 228 KB しか届いてない。

**残り ~20 MB は tee の pipe buffer / 内部 buffer に滞留**。Composer creation のような長時間処理 (10+ 分) では、その間ずっと `Still creating...` が出続けるが flush されない。

### 根本原因

POSIX の標準 buffer 戦略:
- 出力先が **TTY (端末)** = 行 buffer (改行で flush)
- 出力先が **pipe / file** = block buffer (4 KB / 8 KB で flush)

`make ... | tee` の場合:
- `make` の stdout は **pipe** = block buffer
- block buffer は数十 KB〜数 MB まで溜める実装あり
- → 短い行が長時間 flush されない

### 対処

**`stdbuf -oL -eL`** で line buffer を強制:

```bash
make foo 2>&1 | stdbuf -oL -eL tee /tmp/foo.log
```

または:

```bash
unbuffer make foo 2>&1 | tee /tmp/foo.log    # tcl-expect の unbuffer
```

または terraform 限定なら **`-no-color`** で TTY-emulation を切る (もともと色 escape は output 汚染の温床、CI 推奨設定でもある):

```bash
TF_CLI_ARGS_apply="-no-color" make deploy-all 2>&1 | tee /tmp/log
```

ただし `-no-color` は色情報が消えるだけで line buffer 化はしない場合あり。最も確実なのは `stdbuf -oL`。

### 推奨パターン更新 (2026-05-10)

```bash
# bg + line buffer + pipefail + tee
bash -c 'set -o pipefail; make foo 2>&1 | stdbuf -oL -eL tee /tmp/foo.log; echo "exit=$?"'
```

これで:
1. `pipefail` で偽 exit 0 阻止
2. `stdbuf -oL` で line buffer 化 → 走行中もリアルタイム visibility
3. `tee` で全 output 保存
4. 末尾の `echo "exit=$?"` で真の exit code を log にも残す

## 関連

- bg job visibility 問題 (output 0 byte): 上記 §3 の `tee` + `tail -f` パターンで同時解消
- 反省を test 化: 各 step の真の exit code は `_run_*` の戻り値 ≠ 0 を `main()` ループで `print(...FAILED at step ...)` するよう pin (`scripts/setup/deploy_all.py` / `scripts/setup/destroy_all.py`)
