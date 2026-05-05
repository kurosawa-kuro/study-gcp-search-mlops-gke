# docs/conventions/ — 規約・配置・命名の正本セット

**規約・配置・命名** ドキュメントを集約するディレクトリ。`CLAUDE.md` / `docs/architecture/01_仕様と設計.md` 等から参照される。

## 各ファイルの目的

| ファイル | 役割 | メンテ形式 |
|---|---|---|
| [`命名規約.md`](命名規約.md) | 命名規約 (なぜその名前か) — `ml/<機能>/...` / `pipeline/<verb>_job/` / `scripts/{setup,deploy,ops,ci,sql}` 等の命名思想 | 手動 |
| [`Makefile規約.md`](Makefile規約.md) | Make Command Matrix — Canonical Vocabulary | **自動生成** (`tools/generate_makefile_md.sh`) |
| [`Docker配置規約.md`](Docker配置規約.md) | Docker 配置標準 — `infra/run/{services,jobs}/<name>/Dockerfile` の固定配置 | 手動 (検証は `tools/check_docker_layout.py`) |

## 編集ガイド

- `Makefile規約.md` は **手で編集しない**。`tools/generate_makefile_md.sh` を再実行して再生成する (出力先は `docs/conventions/Makefile規約.md`)
- 他は手動編集。変更時は上位 (`CLAUDE.md`) と矛盾していないか確認
- 新規規約ファイルを追加するなら本 dir に配置し、本 README の表にも追記する
