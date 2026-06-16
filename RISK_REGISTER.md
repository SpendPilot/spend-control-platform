# Risk Register

Last updated: 2026-06-16

## Active Risks

| ID | Level | Area | Risk | Mitigation | Status |
| --- | --- | --- | --- | --- | --- |
| R-001 | High | Migration rollout | The additive Alembic changes were not dry-run against PostgreSQL in this environment because no local PostgreSQL runtime was available. | Validate `alembic upgrade head` against PostgreSQL before production rollout. | ACTIVE |
| R-002 | Medium | Legacy documentation | Some non-core docs still reference older role names like `org_admin` or `approver`. | Align legacy docs in a later documentation pass. | ACTIVE |
| R-003 | Medium | UX consolidation | `expenses` and `approvals` now both work, but their long-term overlap should still be simplified in a later polish pass. | Consolidate duplicate review surfaces after stakeholder sign-off on the current flow. | ACTIVE |

## Review Areas

- REVIEW: whether current `approvals` and `expenses` pages should remain separate after UX refinement
- REVIEW: whether the org-owner recurring-request review should be surfaced more directly in the org-owner expenses page
- REVIEW: whether `cost_center` should be mapped into department semantics or retired later
- REVIEW: whether dept-head document visibility needs additional filters beyond department scoping

## Notes

- 2026-06-15: No destructive database migration, repo split, or infra refactor was performed in this run.
- 2026-06-16: Backend validation, frontend validation, and SQLite Alembic validation are green; remaining major uncertainty is PostgreSQL migration validation in a real runtime.
