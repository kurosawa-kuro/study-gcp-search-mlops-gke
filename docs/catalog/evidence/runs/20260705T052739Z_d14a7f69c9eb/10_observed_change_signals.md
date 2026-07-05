# Observed Change Signals

evidence_id: ev.change_signal.summary

This is git history evidence for files that changed often. It is not a defect claim.

| path | commit_count | churn | distinct_authors | last_changed |
|---|---:|---:|---:|---|
| `docs/tasks/TASKS_ROADMAP.md` | 36 | 2080 | 1 | `2026-05-12T00:02:11+09:00` |
| `"docs/architecture/03_\345\256\237\350\243\205\343\202\253\343\202\277\343\203\255\343\202\260.md"` | 29 | 3009 | 1 | `2026-05-12T00:19:23+09:00` |
| `docs/tasks/TASKS.md` | 25 | 838 | 1 | `2026-05-12T00:02:11+09:00` |
| `"docs/architecture/01_\344\273\225\346\247\230\343\201\250\350\250\255\350\250\210.md"` | 20 | 3180 | 1 | `2026-05-12T00:19:23+09:00` |
| `CLAUDE.md` | 19 | 491 | 1 | `2026-05-12T00:02:11+09:00` |
| `README.md` | 16 | 1091 | 1 | `2026-05-12T00:02:11+09:00` |
| `"docs/runbook/04_\346\244\234\350\250\274.md"` | 14 | 618 | 1 | `2026-05-11T23:41:20+09:00` |
| `"docs/runbook/05_\351\201\213\347\224\250.md"` | 12 | 1471 | 1 | `2026-05-11T23:41:20+09:00` |
| `scripts/setup/deploy_all.py` | 11 | 541 | 1 | `2026-05-11T23:05:33+09:00` |
| `Makefile` | 11 | 386 | 1 | `2026-05-11T23:05:33+09:00` |
| `"docs/tasks/02_\347\247\273\350\241\214\343\203\255\343\203\274\343\203\211\343\203\236\343\203\203\343\203\227.md"` | 10 | 268 | 1 | `2026-05-06T01:49:59+09:00` |
| `"7/study-hybrid-search-gke/docs/architecture/01_\344\273\225\346\247\230\343\201\250\350\250\255\350\250\210.md"` | 7 | 972 | 1 | `2026-05-06T01:21:00+09:00` |
| `scripts/setup/destroy_all.py` | 7 | 429 | 1 | `2026-05-11T23:05:33+09:00` |
| `tests/unit/scripts/test_deploy_all_step_timing.py` | 7 | 344 | 1 | `2026-05-11T23:05:33+09:00` |
| `AGENTS.md` | 7 | 273 | 1 | `2026-05-06T20:25:51+09:00` |
| `tests/integration/workflow/test_destroy_all_contract.py` | 7 | 210 | 1 | `2026-05-10T21:43:23+09:00` |
| `tests/integration/workflow/test_deploy_all_contract.py` | 7 | 134 | 1 | `2026-05-11T23:05:33+09:00` |
| `7/study-hybrid-search-gke/Makefile` | 6 | 586 | 1 | `2026-05-06T01:24:26+09:00` |
| `"3/study-hybrid-search-local/docs/01_\344\273\225\346\247\230\343\201\250\350\250\255\350\250\210.md"` | 6 | 416 | 1 | `2026-05-05T20:55:17+09:00` |
| `3/study-hybrid-search-local/Makefile` | 6 | 202 | 1 | `2026-05-06T00:12:45+09:00` |

## Notes

- churn = added + deleted lines from `git log --numstat`.
- binary file churn is counted as 0 when git reports `-`.
