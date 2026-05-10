---
name: doc-sync
description: 'Synchronize canonical and historical documentation after policy or scope changes. Use when refactoring duplicate content, updating historical notes, and reflecting corrections into top-level README and docs hubs.'
argument-hint: 'What policy or scope change should be propagated?'
---

# Documentation Sync

## What This Skill Produces

- A consistent set of documentation updates across root README, docs hubs, and any relevant historical / decision documents.
- Reduced duplication by keeping detailed content in authoritative locations and linking from summaries.
- A short verification report that confirms key terms and policy statements are aligned.

## When to Use

- A canonical policy changed (例: required tools, forbidden tools, scope constraints, 中核 5 要素 のいずれか)。
- 重複しているセクションを 1 箇所に集約したい。
- `docs/tasks/TASKS_ROADMAP.md` / `docs/tasks/TASKS.md` を更新した後にエントリポイント (root `README.md` / `CLAUDE.md`) へ反映したい。
- Review feedback で「top-level docs と historical docs が drift している」と指摘された。

## Authority Order (このリポの正本順位)

正本順位 (high → low):

1. `docs/tasks/TASKS_ROADMAP.md` — 長期 backlog / 過去判断履歴
2. `docs/tasks/TASKS.md` — current sprint
3. `docs/architecture/01_仕様と設計.md` — canonical 仕様
4. `docs/architecture/03_実装カタログ.md` — 実装スナップショット
5. `README.md` — プロジェクト概要 / 技術スタック / 非負制約
6. `CLAUDE.md` / `AGENTS.md` — agent 運用ルール

低位ドキュメントが高位と矛盾していたら **低位を高位に揃える**。逆をやらない。

## Approach

1. ユーザの input から「変更されたポリシー / scope」を 1〜2 文で要約。
2. 上の正本順位のうち、**ポリシーが具体化されている最上位ファイル** を特定。
3. そのファイルの該当節を読み、他のドキュメント (`README.md` / `CLAUDE.md` / `docs/architecture/03_実装カタログ.md` 等) で同じトピックに触れている節を全件 grep。
4. drift があれば: 詳細は最上位ファイルへ集約、低位は 1〜3 行のサマリ + 最上位への link に置き換える。
5. 関連する `docs/decisions/<NNNN>.md` (ADR) があれば「決定の根拠」を historical note として ADR に残し、TASKS / TASKS_ROADMAP には現在進行形の状態のみ書く。
6. 最後に verification report:
   - drift 残存チェック: `rg -n "<key term>" docs/ README.md CLAUDE.md` で重複定義が複数 → ❌
   - link 切れ: 相対パスが正しいか
   - 削除した古い記述に外部 link が来ていないか

## Output

- 変更ファイル一覧 (path: 行範囲: 変更概要)
- verification report (PASS / FAIL + drift 検出箇所)

## Hard rules

- 中核 5 要素 (Elasticsearch / multilingual-e5 / Vertex Vector Search / RRF / LightGBM LambdaRank) の記述を変更する提案は user の明示的合意なしに出さない。
- 古い概念 (Phase 形式 / Meilisearch / `SEMANTIC_BACKEND=bq_vector` 等) が drift で残っていたら **flag** する。当該概念の復活提案ではなく削除提案として扱う。
