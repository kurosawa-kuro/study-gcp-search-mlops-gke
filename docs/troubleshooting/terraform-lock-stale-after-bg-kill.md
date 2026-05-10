# Terraform state lock 残存 (bg job kill 後)

## 症状

`make destroy-all` / `make deploy-all` を bg で実行中に kill (SIGTERM/SIGKILL) → 次回 terraform 操作で:

```
Error: Error acquiring the state lock
Error message: writing "gs://<project>-tfstate/.../default.tflock" failed:
googleapi: Error 412: At least one of the pre-conditions you specified did
not hold., conditionNotMet
Lock Info:
  ID:        1778332028753123
  Path:      gs://<project>-tfstate/.../default.tflock
  Operation: OperationTypeApply
  Who:       ubuntu@<host>
  Version:   1.14.8
  Created:   <時刻>
```

= terraform プロセスが lock を release する前に kill された結果、GCS 上に lock object が残置。

## 推奨手順

### 1. 走行中の terraform process がないことを確認

```bash
pgrep -af "terraform.*apply|terraform.*destroy"  # 何も出なければ OK
```

何か残っていれば `kill -TERM <pid>` で止め、release を待つ (~10s)。

### 2. force-unlock

```bash
terraform -chdir=infra/terraform/environments/dev force-unlock -force <LOCK_ID>
```

### 3. 自動化 (推奨)

```bash
TERRAFORM_STATE_FORCE_UNLOCK=1 make destroy-all
```

`scripts/domain/terraform/lock.py` が:

1. `Error acquiring the state lock` を検知
2. lock ID を parse (ANSI escape strip + 緩い prefix で、罫線 `│` + ANSI color 入り output に対応)
3. `force-unlock -force <id>` を発行
4. 元のコマンドを 1 度だけ retry

を一連で実行する。

## 設計上の防止策

- `scripts/domain/terraform/lock.py` の lock ID parser を ANSI escape 入りの実出力でも parse できるように修正済 (2026-05-10)
- `tests/unit/scripts/test_terraform_lock.py` に実 ANSI escape 入りの test を pin

## 過去事故

| 日付 | 事象 | 教訓 |
|---|---|---|
| 2026-05-09 | bg destroy-all kill → lock 残置 → 翌日 destroy-all が step 6 (flip-deletion-protection) で fail。`TERRAFORM_STATE_FORCE_UNLOCK=1` 設定したのに lock parser が ANSI escape で fail し自動 unlock が走らず、手動 force-unlock が必要だった | parser を実出力で test 駆動 (test 上の ANSI escape literal は本物の `\x1b` を含めること、表示文字列の偽 ANSI は偽 PASS の温床) |

## 関連

- `scripts/domain/terraform/lock.py` (実装)
- `tests/unit/scripts/test_terraform_lock.py` (test、ANSI escape pin)
- `docs/troubleshooting/eck-license-reconcile-stall.md` (cluster destroy する時の判断指針)
- `docs/troubleshooting/bg-pipe-fake-exit-zero.md` (bg + pipe 偽 exit 0 罠)
