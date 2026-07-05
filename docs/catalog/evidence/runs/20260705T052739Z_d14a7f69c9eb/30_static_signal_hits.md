# Static Signal Hits

This is a machine-generated signal inventory, not a decision.
Every row points back to grep evidence.

| query_id | hit_state | hits | evidence_ref | follow_up |
|---|---|---:|---|---|
| `todos` | `matched` | 6 | `file=evidence/grep/01_todos.md query_id=todos` | review matching lines before deciding |
| `job_lifecycle` | `matched` | 1055 | `file=evidence/grep/02_job_lifecycle.md query_id=job_lifecycle` | review matching lines before deciding |
| `env_secret` | `matched` | 613 | `file=evidence/grep/03_env_secret.md query_id=env_secret` | review matching lines before deciding |
| `high_risk_ops` | `matched` | 602 | `file=evidence/grep/04_high_risk_ops.md query_id=high_risk_ops` | review matching lines before deciding |
| `auth_permission` | `matched` | 759 | `file=evidence/grep/05_auth_permission.md query_id=auth_permission` | review matching lines before deciding |
| `infra_surface` | `matched` | 1620 | `file=evidence/grep/06_infra_surface.md query_id=infra_surface` | review matching lines before deciding |
| `change_signal:docs/tasks/TASKS_ROADMAP.md` | `observed` | 36 | `file=evidence/10_observed_change_signals.md path=docs/tasks/TASKS_ROADMAP.md` | inspect change history before editing |
| `change_signal:"docs/architecture/03_\345\256\237\350\243\205\343\202\253\343\202\277\343\203\255\343\202\260.md"` | `observed` | 29 | `file=evidence/10_observed_change_signals.md path="docs/architecture/03_\345\256\237\350\243\205\343\202\253\343\202\277\343\203\255\343\202\260.md"` | inspect change history before editing |
| `change_signal:docs/tasks/TASKS.md` | `observed` | 25 | `file=evidence/10_observed_change_signals.md path=docs/tasks/TASKS.md` | inspect change history before editing |
| `change_signal:"docs/architecture/01_\344\273\225\346\247\230\343\201\250\350\250\255\350\250\210.md"` | `observed` | 20 | `file=evidence/10_observed_change_signals.md path="docs/architecture/01_\344\273\225\346\247\230\343\201\250\350\250\255\350\250\210.md"` | inspect change history before editing |
| `change_signal:CLAUDE.md` | `observed` | 19 | `file=evidence/10_observed_change_signals.md path=CLAUDE.md` | inspect change history before editing |

## Guardrail

- Static signal entries are observations only. Decision Catalog claims still need explicit `evidence_ref` values.
