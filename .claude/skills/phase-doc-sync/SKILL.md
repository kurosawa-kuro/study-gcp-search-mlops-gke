---
name: phase-doc-sync
description: 'Synchronize canonical and historical documentation after policy or scope changes. Use when refactoring duplicate content, updating historical notes, and reflecting corrections into top-level README and docs hubs.'
argument-hint: 'What policy or scope change should be propagated?'
---

# Phase Documentation Sync

## What This Skill Produces

- A consistent set of documentation updates across root README, docs hubs, and any relevant historical documents.
- Reduced duplication by keeping detailed content in authoritative locations and linking from summaries.
- A short verification report that confirms key terms and policy statements are aligned.

## When to Use

- A canonical policy changed (for example, required tools, forbidden tools, or scope constraints).
- You need to refactor duplicate sections across docs.
- You updated a roadmap or adjustment plan and need to reflect it into repository entry points.
- Review feedback says top-level docs and historical docs are drifting.

## Workflow

1. Define the change scope.
   - Record what changed, effective date, and whether it is global or historical-scope only.
   - Decide canonical source documents before editing.

2. Map impacted documents.
   - Identify likely entry points first: root README, docs index/hubs, and the relevant task/roadmap docs.
   - Search for old terms and statements to build an edit list.

3. Classify each edit target.
   - Keep canonical details in authoritative docs.
   - Keep top-level docs concise and link to authoritative docs.
   - Mark repeated long sections as dedup candidates.

4. Apply edits in dependency order.
   - Update canonical docs first.
   - Update root and hub docs second to reflect the canonical version.
   - Replace repeated paragraphs with short summaries plus pointers.

5. Run consistency checks.
   - Verify the same policy wording appears everywhere it should.
   - Verify removed/deprecated tools are no longer presented as active guidance.
   - Verify ownership is clear: root is canonical navigation, historical docs are clearly marked when they differ.

6. Finalize with a concise change note.
   - Summarize what was deduplicated.
   - Summarize what was propagated.
   - List any intentional exceptions.

## Decision Points

- Global vs historical/local change:
  - Global: update root README and all relevant docs hubs, then affected historical docs.
  - Historical/local: update the local docs first; update root only if discovery/navigation text changes.

- Duplicate section handling:
  - If duplicate content is normative and long, keep one canonical version and replace others with links.
  - If duplicate content is brief and navigational, keep concise mirrored summaries.

- Conflicting statements found:
  - Treat canonical root docs as source of truth unless the change is explicitly historical/archive-only.
  - Align hub text to canonical wording and mark exceptions clearly.

## Completion Criteria

- No contradictory policy statements across root, hub, and phase docs.
- Top-level docs contain navigation and summary, not long duplicated operational detail.
- Deprecated guidance is removed or explicitly marked historical.
- Key term checks pass (for example, removed tool names only appear in historical/archive context if expected).
- A short final note captures scope, updated files, and open follow-ups.

## Suggested Verification Commands

- Find stale terms:
  - `rg -n "<old-term>|<deprecated-tool>|<old-policy-phrase>" README.md docs/ 1/ 2/ 3/ 4/ 5/ 6/ 7/`
- Find duplicated headings/phrases candidates:
  - `rg -n "^## |^### " README.md docs/`

Adjust search terms to the current change request.
