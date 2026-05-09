# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済み実装ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)。

---

## 本 sprint scope (2026-05-09)

- 対象: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §1 #4 / #5 と Wave 5 / Wave 8 の残件
- **scope outside**: Wave 9 (独自ドメイン + HTTPS + DNS) — user 指示で本 sprint 除外

---

## 完成定義 (Definition of Done)

下記 2 項目すべてが ✅ になれば本 sprint 完了。完了済 (T3 / T4 / T5) は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §7.3 へ移管済。

| ID | タスク | 完了条件 | 着手コマンド / 手順 |
|---|---|---|---|
| T1 ⚠️ | M-Wave5 live 検証通し | `make verify-live-acceptance` が PASS | `make verify-live-acceptance` (要 `make deploy-all` 済 mlops-dev-a) |
| T2 | runbook 2 本 drift 解消 | [`../runbook/04_検証.md`](../runbook/04_検証.md) と [`../runbook/05_運用.md`](../runbook/05_運用.md) が現 state (Wave 6 後の ES + 4 軸 API) と一致 | 03_実装カタログと突き合わせて差分修正 |

⚠️ = canonical 必須項目。[`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) §0.1 ゴール劣化禁止対象。

進め方: **T2 (doc 編集、live 不要) → T1 (live 環境前提)**。T1 は cluster 生死を `kubectl get nodes` / `make ops-search-components` で確認してから。deploy-all を最初に走らせない。

---

## 参照

- 完了済み実装スナップショット + マイルストーン履歴: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- Wave / 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証ゲート定義 (V1-V6): [`../runbook/04_検証.md`](../runbook/04_検証.md)
- PDCA / 運用手順: [`../runbook/05_運用.md`](../runbook/05_運用.md)
