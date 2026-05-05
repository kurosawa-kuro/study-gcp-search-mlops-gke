# docs

ルート `docs/` は、**Phase 7 を canonical とした補助ハブ**です。  
現役コードの正本は **repo ルート** にあり、ここには phase 横断の整理メモ・導線・規約を置きます。

トップ入口:

- ルート: [`../README.md`](../README.md)
- 現役正本: [README.md](README.md)

## まず読むファイル

- [`../7/study-hybrid-search-gke/docs/tasks/TASKS.md`](../7/study-hybrid-search-gke/docs/tasks/TASKS.md)
  - 現在の sprint / 実装進捗の正本
- [`architecture/01_仕様と設計.md`](architecture/01_仕様と設計.md)
  - 現役の仕様と設計
- [`runbook/05_運用.md`](runbook/05_運用.md)
  - 現役の運用と local / live 検証導線
- [`conventions/`](conventions/README.md) — 規約・配置・命名の正本セット (5 ファイル + 索引 README)
  - `conventions/命名規約.md` — フォルダ名・ファイル名・役割の共通規約
  - `conventions/フォルダ-ファイル.md` — Phase 1-7 を 1 枚で見る構造索引
  - `conventions/スクリプト規約.md` — scripts 命名標準
  - `conventions/Makefile規約.md` — Make Command Matrix (auto-generated)
  - `conventions/Docker配置規約.md` — Dockerfile / compose 関連の共通ルール
- `archive/README.md`
  - 過去ログの退避方針
- `phases/README.md`
  - 旧 phase 群の補助入口

## 位置付け

- **現役正本は Phase 7 配下**
- ルート `docs/` は、phase 横断の管理情報と移行メモを置く場所
- 旧 Phase 1-6 は、比較教材 / 学習履歴 / archive 候補として扱う
- 実装詳細・運用・検証は、常に Phase 7 配下を優先参照する

## 補助資料

- [`conventions/フォルダ-ファイル.md`](conventions/フォルダ-ファイル.md) — Phase 1-7 構造索引 + 各要素の役割と実装形態 (旧 `パイプラインとジョブ.md` を統合)
- `archive/パイプラインとジョブ.md` — 旧版 (2026-04-26 archived、`conventions/フォルダ-ファイル.md` の前身)
