#!/usr/bin/env bash
# SessionStart hook: show the head of the current sprint/task document so the
# user (and the model) start each session with the active sprint in mind.
#
# Resolution: walk up from $CLAUDE_PROJECT_DIR (set by Claude Code) looking
# for the repo root (a dir containing Makefile + pyproject.toml). If found,
# show the first 50 lines of TASKS.md. Prefer `docs/tasks/TASKS.md`, fall
# back to `docs/TASKS.md`. If not in repo root, do nothing.
#
# This hook prints to stdout (visible to the user). It must be fast (<1s)
# and never block the session.

set -euo pipefail

# Read the JSON event from stdin (Claude Code sends it but we only need cwd).
input=$(cat 2>/dev/null || true)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null || true)
[ -z "$cwd" ] && cwd="${CLAUDE_PROJECT_DIR:-$PWD}"

# Walk up to find the repo root (Makefile + pyproject.toml).
dir="$cwd"
repo_root=""
while [ "$dir" != "/" ] && [ -n "$dir" ]; do
  if [ -f "$dir/Makefile" ] && [ -f "$dir/pyproject.toml" ]; then
    repo_root="$dir"
    break
  fi
  dir=$(dirname "$dir")
done

[ -z "$repo_root" ] && exit 0

tasks_md=""
if [ -f "$repo_root/docs/tasks/TASKS.md" ]; then
  tasks_md="$repo_root/docs/tasks/TASKS.md"
elif [ -f "$repo_root/docs/TASKS.md" ]; then
  tasks_md="$repo_root/docs/TASKS.md"
fi

[ -z "$tasks_md" ] && exit 0

repo_name=$(basename "$repo_root")
printf '## Current sprint — %s (%s)\n\n' "$repo_name" "${tasks_md#$repo_root/}"
head -50 "$tasks_md"
