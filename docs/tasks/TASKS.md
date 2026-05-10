# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済の実装ログ + マイルストーン履歴 + incident memo は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §6 / §7.3 / §7.4 を正本。

---

## sprint 状態 (2026-05-10 終了時点)

**本 sprint 完了**:
- M-Wave5 (継続改善サイクル MVP) PASS、verify-live-acceptance 22.68s
- M-Wave8.5 (Phase 概念完全撤廃) 達成、`grep -rE "Phase [0-9]" docs/ tests/` ADR 除外で 0 件
- M-Wave8.6 Phase 1+2+3 + 後段 caller migration 完了 (orchestrator ドメイン分離 / adapters 構造 / `subprocess.run([cli, ...])` → `cli_run(...)` 全件)
- M-Wave7 Makefile 本格整理 (Phase Support Matrix 撤去 / `mk/base.mk` 削除 / `deploy-all-direct` + `verify-all` legacy alias 撤去 / `destroy-phase7-learning` → `destroy-coast-down` rename / `phase7-ml-base:local` → `mlops-ml-base:local` / `.SHELLFLAGS pipefail` 追加)
- GCP リソース ID rename: `phase7-synonym` → `mlops-synonym` (Memorystore + Secret + ExternalSecret)
- C4 Makefile `python -u -m` 統一 (line buffer 強制、bg-pipe 罠予防)
- PMLE 学習 doc 8 章新設

cluster は **destroy 完了** (永続 VVS Index/Endpoint のみ残置、コスト止血済)。次セッションは clean state から `make deploy-all` 一発で復活可能。

## 残課題 (次 sprint candidates、優先度順)

| # | 内容 | コスト | 状態 |
|---|---|---|---|
| 1 | M-Wave8.7 ES production 化 (HTTPS+password) + M-Wave9 (独自ドメイン+HTTPS+DNS) | 1 sprint | ⏸ ドメイン購入後 |

詳細は [`TASKS_ROADMAP.md §1 / §2`](TASKS_ROADMAP.md)。

## 参照

- 完了済: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証 / PDCA: [`../runbook/04_検証.md`](../runbook/04_検証.md) / [`../runbook/05_運用.md`](../runbook/05_運用.md)
- troubleshooting: [`../troubleshooting/`](../troubleshooting/)
- PMLE 学習 doc: [`../pmle-learning-notes.md`](../pmle-learning-notes.md)
