# TASKS — current sprint dashboard

権威順位は [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) を参照。ここは **短周期の作業メモ・検証ログの置き場**。

---

## Latest session (2026-05-06)

**目的**: 現在スプリントの進行管理を軽量に維持する（完了済み詳細は `03_実装カタログ.md` へ集約）。

**ROADMAP**: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) が優先。完了済み実行ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) を参照。

### 現在地（2026-05-06 20:21 JST）

- **完了済み（要点）**:
  - Wave 6 (Elasticsearch on GKE/ECK) は live 収束済み
  - `/api/v1/search` の 3 系統寄与は all non-zero を確認済み
  - 学習再実行と精度ゲート (`ndcg_at_10=1.0`) は達成済み
  - 詳細ログは [`../architecture/03_実装カタログ.md`「直近完了作業ログ」](../architecture/03_実装カタログ.md) に転記済み

- **進行中（短期）**:
  - Wave 8: canonical docs の最終同期 (`01/03/runbook`)
  - `make verify-live-acceptance` の最終通し

### 優先タスク

- [ ] `verify-live-acceptance` 一式を再通し
- [ ] `runbook/04_検証.md` と `runbook/05_運用.md` の drift 解消
- [ ] Wave 9 事前準備（独自ドメイン + HTTPS + DNS の実行計画）

### 参照

- 詳細な完了済みログ: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- 長期課題・Wave管理: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
