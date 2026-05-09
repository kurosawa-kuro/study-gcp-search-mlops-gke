# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済み実装ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)。

---

## 本 sprint scope (2026-05-09)

- 対象: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §1 #4 / #5 と Wave 5 / Wave 8 の残件
- **scope outside**: Wave 9 (独自ドメイン + HTTPS + DNS) — user 指示で本 sprint 除外

---

## 完成定義 (Definition of Done)

下記 5 項目すべてが ✅ になれば本 sprint 完了:

| ID | タスク | 完了条件 | 着手コマンド / 手順 |
|---|---|---|---|
| T1 ⚠️ | M-Wave5 live 検証通し | `make verify-live-acceptance` が PASS | `make verify-live-acceptance` (要 `make deploy-all` 済 mlops-dev-a) |
| T2 | runbook 2 本 drift 解消 | [`../runbook/04_検証.md`](../runbook/04_検証.md) と [`../runbook/05_運用.md`](../runbook/05_運用.md) の記述が現 state (Wave 6 後の ES + 4 軸 API) と一致 | 03_実装カタログと突き合わせて差分修正 |
| T3 | ROADMAP §1 / §5 表 drift 解消 | §1 表に Wave 9 scope outside / §5 表が §2 各 Wave の `[x]`/`[ ]` と一致 | ✅ 2026-05-09 本コミットで反映済 |
| T4 | M-Wave1 (API 4 軸) 判定固定 | API 4 軸 contract test PASS を確認 → §1 #4 と M-Wave1 を ✅ 化、または残作業を明記 | `uv run pytest tests/integration/parity/test_api_route_prefixes.py` |
| T5 | M-Wave0 (Makefile 止血) 棚卸し | Wave 0 完了条件 = Makefile 内 5 行超 shell block が **0 件**。現状件数を §5 に明記し、移送 PR を切るか「次 sprint」と判定 | `awk '/\\$/' Makefile` で違反 target 抽出 → `scripts/<folder>/<module>.py` 移送 → 1 行 wrapper 化 |

⚠️ = canonical 必須項目。[`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) §0.1 ゴール劣化禁止対象。

---

## 現状把握 (2026-05-09 時点)

| 領域 | 実装側 | 検証側 | 判定 |
|---|---|---|---|
| Wave 0 (Makefile 止血) | Makefile に 5 行超 shell block が複数残存 (継続行 11 件) | — | ⏳ |
| Wave 1 (API 4 軸) | `app/main.py` で `/api/v1` `/ops` `/ui` prefix 分離済 / `tests/integration/parity/test_api_route_prefixes.py` 存在 / IAP policy あり | contract test 通し未確認 | ⏳ → T4 で確定 |
| Wave 2-4 (Event schema / EventWriter / LightGBM 接続) | §2 各 Wave [x] 完了 | unit/contract PASS | ✅ (§5 表は drift) |
| Wave 5 (継続改善サイクル MVP) | 配線完了 / `ndcg_at_10=1.0` 達成 | `make verify-live-acceptance` 最終通し未済 | 🟡 |
| Wave 6 (Elasticsearch on GKE) | 完了 | `ops-search-components` all non-zero 確認済 | ✅ |
| Wave 7 (Makefile 本格整理) | Wave 1-6 完了後着手予定 | — | ⏳ (Wave 0 → Wave 1 を先に) |
| Wave 8 (docs 再統合) | 大半 [x] 済 | runbook 2 本 drift / §5 表 drift | ⏳ → T2/T3 で解消 |

---

## 進め方の推奨順序

1. ~~**T3**: §1 / §5 表 drift 解消~~ ✅ 2026-05-09 完了
2. **T4** (低コスト、5 分): Wave 1 を contract test で判定確定 → §1 #4 と §5 M-Wave1 を更新
3. **T1** (中コスト、live 環境必要): `make verify-live-acceptance` 通し → M-Wave5 ✅
4. **T2** (中コスト、doc 編集): runbook 2 本を T1 の実走結果で同期
5. **T5** (高コスト、構造変更): Makefile 止血。完成にコストがかかる場合は次 sprint 切り出し可

---

## 参照

- 完了済み実装スナップショット: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- Wave / 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証ゲート定義 (V1-V6): [`../runbook/04_検証.md`](../runbook/04_検証.md)
- PDCA / 運用手順: [`../runbook/05_運用.md`](../runbook/05_運用.md)
