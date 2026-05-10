---
name: doc-sync
description: 'Synchronize canonical and historical documentation after policy or scope changes. Use when refactoring duplicate content, updating historical notes, and reflecting corrections into top-level README and docs hubs.'
argument-hint: 'What policy or scope change should be propagated?'
---

# Documentation Sync (GitHub-side mirror)

`.claude/skills/doc-sync/SKILL.md` の GitHub agent 側 mirror。内容は同じポリシーで運用する。

## What This Skill Produces

- A consistent set of documentation updates across root README, docs hubs, and any relevant historical / decision documents.
- Reduced duplication by keeping detailed content in authoritative locations and linking from summaries.
- A short verification report that confirms key terms and policy statements are aligned.

## When to Use

- A canonical policy changed (例: required tools, forbidden tools, scope constraints, 中核 5 要素 のいずれか)。
- 重複しているセクションを 1 箇所に集約したい。
- `docs/tasks/TASKS_ROADMAP.md` / `docs/tasks/TASKS.md` を更新した後にエントリポイント (root `README.md` / `CLAUDE.md` / `AGENTS.md`) へ反映したい。
- Review feedback で「top-level docs と historical docs が drift している」と指摘された。

## Authority Order

1. `docs/tasks/TASKS_ROADMAP.md`
2. `docs/tasks/TASKS.md`
3. `docs/architecture/01_仕様と設計.md`
4. `docs/architecture/03_実装カタログ.md`
5. `README.md`
6. `CLAUDE.md` / `AGENTS.md`

低位ドキュメントが高位と矛盾していたら低位を高位に揃える。

## Approach

1. ユーザ input から「変更されたポリシー / scope」を 1〜2 文で要約。
2. 上の正本順位のうち、ポリシーが具体化されている最上位ファイルを特定。
3. そのファイルの該当節を読み、他ドキュメントで同じトピックに触れている節を全件 grep。
4. drift があれば、詳細は最上位に集約、低位はサマリ + link 化。
5. 関連 ADR (`docs/decisions/<NNNN>.md`) があれば historical note として ADR に残す。
6. verification report (drift 残存 / link 切れチェック)。

## Hard rules

- 中核 5 要素 (Elasticsearch / multilingual-e5 / Vertex Vector Search / RRF / LightGBM LambdaRank) の記述を変更する提案は user の明示的合意なしに出さない。
- 古い概念 (Phase 形式 / Meilisearch / `SEMANTIC_BACKEND=bq_vector` 等) が drift で残っていたら flag する。
