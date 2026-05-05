# docs

本プロジェクトの仕様 / 設計 / 運用 / 検証 / 規約を集約するハブ。

## まず読むファイル

- [`tasks/TASKS.md`](tasks/TASKS.md) — current sprint の正本 (新セッションで最初に読む)
- [`tasks/TASKS_ROADMAP.md`](tasks/TASKS_ROADMAP.md) — 長期 backlog + 決定的仕様 + Wave 計画
- [`architecture/01_仕様と設計.md`](architecture/01_仕様と設計.md) — 仕様 + アーキテクチャ canonical
- [`architecture/03_実装カタログ.md`](architecture/03_実装カタログ.md) — 実装物スナップショット
- [`runbook/05_運用.md`](runbook/05_運用.md) — PDCA loop + STEP 詳細 + インシデント対応
- [`runbook/04_検証.md`](runbook/04_検証.md) — 検証ゲート定義 + 「OK」判定基準

## ディレクトリ構成

| ディレクトリ | 内容 |
|---|---|
| [`architecture/`](architecture/) | 仕様 + 実装カタログ |
| [`runbook/`](runbook/) | 検証ゲート + 運用手順 |
| [`tasks/`](tasks/) | current sprint + 長期 backlog |
| [`decisions/`](decisions/) | ADR (恒久対処ギャップの記録、0001〜0008) |
| [`conventions/`](conventions/) | 命名 / 配置 / Make / Docker の規約セット |

## 権威順位 (矛盾時の勝者)

```
TASKS_ROADMAP.md  >  TASKS.md  >  01_仕様と設計.md  >  README.md  >  CLAUDE.md
(長期 backlog)       (current sprint) (機能仕様+設計)    (入口)        (Claude 向けガイド)
```

恒久的な判断履歴は [`decisions/`](decisions/) (ADR 形式)。
