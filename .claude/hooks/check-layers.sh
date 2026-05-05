#!/usr/bin/env bash
# PostToolUse hook (matcher: Edit|Write|MultiEdit): if the edited file lives
# in a Port-Adapter sensitive area, run `make check-layers` in the background
# and only surface the result if it fails.
#
# Sensitive areas (from scripts/ci/layers.py):
#   - app/services/  (Port + adapter + noop)
#   - app/composition_root.py (DI excluded but watch leaks)
#   - app/api/{routers,mappers,middleware}/
#   - app/domain/, app/schemas/
#   - ml/<feature>/ports/, ml/<feature>/adapters/
#   - pipeline/<job>/ports/, pipeline/dags/
#   - scripts/ci/layers.py itself (rules edits)
#
# Other edits (infra/terraform, docs, tests) skip the check — Terraform
# apply is a human decision, docs/tests don't trigger the boundary.

set -euo pipefail

input=$(cat 2>/dev/null || true)
file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)
[ -z "$file_path" ] && exit 0

# Only react to sensitive paths.
case "$file_path" in
  */app/services/*|*/app/composition_root.py|*/app/api/*|*/app/domain/*|*/app/schemas/*) ;;
  */ml/*/ports/*|*/ml/*/adapters/*) ;;
  */pipeline/*/ports/*|*/pipeline/dags/*) ;;
  */scripts/ci/layers.py) ;;
  *) exit 0 ;;
esac

# Walk up to find the repo root.
dir=$(dirname "$file_path")
repo_root=""
while [ "$dir" != "/" ] && [ -n "$dir" ]; do
  if [ -f "$dir/Makefile" ] && [ -f "$dir/pyproject.toml" ]; then
    repo_root="$dir"
    break
  fi
  dir=$(dirname "$dir")
done

[ -z "$repo_root" ] && exit 0

# Background check — only output if check-layers fails.
log_file="$repo_root/.claude-check-layers.log"
(
  cd "$repo_root"
  if ! make check-layers > "$log_file" 2>&1; then
    echo "[check-layers FAILED] $repo_root" >&2
    tail -20 "$log_file" >&2
  fi
) </dev/null >/dev/null 2>&1 &
disown

exit 0
