# .codex

Repo-local notes for working in this repository with Codex.

## What Codex Actually Reads

- [`AGENTS.md`](../AGENTS.md) is the primary repo charter.
- [`CLAUDE.md`](../CLAUDE.md) remains the richest constraint/history doc and is worth consulting when a task touches architecture, orchestration, or incident-driven guardrails.
- Files in `.codex/` are repo-local operational notes for humans and future agents. They are not hooks and are not auto-executed.

## What Codex Does Not Natively Reuse

- `.claude/hooks/*`
- `.claude/settings.json`
- `.claude/commands/*`

Those are Claude Code conventions. When they contain useful intent, mirror the intent here and in `AGENTS.md`.

## Canonical Usage In This Repo

1. Read [`AGENTS.md`](../AGENTS.md) first.
2. Read [`docs/tasks/TASKS.md`](../docs/tasks/TASKS.md) for current sprint context.
3. Use [`playbooks.md`](playbooks.md) to emulate the useful parts of the old Claude hooks.

## Current Policy

- Repo root is canonical.
- Do not assume `.claude` behavior runs automatically under Codex.
- Prefer explicit local verification commands over invisible automation.
