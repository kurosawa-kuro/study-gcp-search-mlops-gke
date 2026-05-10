# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済み実装ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)。

---

## sprint 状態 (2026-05-10)

**本 sprint ✅ クローズ**。M-Wave5 (継続改善サイクル MVP) PASS、cluster destroy 完了 (永続 VVS 残置)。詳細は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §6 (直近完了ログ) / §7.3 (マイルストーン履歴) / §7.4 (incident memo)。

## 次 sprint candidates (優先度順)

- **M-Wave8.7** ES production 化 (HTTPS + password auth) — 詳細: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §2 Wave 8.7
- **M-Wave8.5** Phase 概念完全撤廃 — 詳細: §2 Wave 8.5
- **M-Wave8.6 Phase 3** orchestrator ドメイン分離 (`scripts/infra/*` → `scripts/domain/`、subprocess wrapper を `scripts/adapters/`) — 詳細: §2 Wave 8.6
- **C4** Makefile target に `stdbuf -oL` 組込 — Wave 7 (Makefile 整理) の延長
- **M-Wave9** 独自ドメイン + HTTPS + DNS — scope outside、user 指示で除外継続

## 参照

- 完了済み実装スナップショット + マイルストーン履歴 + incident memo: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- Wave / 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証ゲート / PDCA: [`../runbook/04_検証.md`](../runbook/04_検証.md) / [`../runbook/05_運用.md`](../runbook/05_運用.md)
- troubleshooting: [`../troubleshooting/`](../troubleshooting/) (eck-license-reconcile-stall / terraform-lock-stale-after-bg-kill / bg-pipe-fake-exit-zero)
