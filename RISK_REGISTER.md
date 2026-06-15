# Risk Register

Last updated: 2026-06-15

## Active Risks

| ID | Level | Area | Risk | Mitigation | Status |
| --- | --- | --- | --- | --- | --- |
| R-001 | High | Validation environment | Frontend build, lint, and typecheck could not be executed locally because Node package-manager binaries are unavailable in the current shell environment. | Re-run `npm run build` and `npm run lint` once Node tooling is available. | ACTIVE |
| R-002 | High | Migration rollout | The additive Alembic changes were not dry-run against PostgreSQL in this environment. | Validate `alembic upgrade head` against PostgreSQL before production rollout. | ACTIVE |
| R-003 | Medium | UI completeness | The role-aware frontend is a functional baseline but still needs UX polish against the full target spec. | Treat current UI as working baseline and continue iterative refinement after build validation. | ACTIVE |
| R-004 | Medium | Legacy documentation | Some non-core docs still reference older role names like `org_admin` or `approver`. | Align legacy docs in a later documentation pass. | ACTIVE |
| R-005 | Medium | Cleanup timing | Cleanup deletions were intentionally deferred to avoid removing product or deployment assets before broader validation. | Keep cleanup plan conservative until frontend and migration validation are complete. | ACTIVE |

## Review Areas

- REVIEW: whether current `approvals` and `expenses` pages should remain separate after UX refinement
- REVIEW: whether the org-owner recurring-request review should be surfaced more directly in the org-owner expenses page
- REVIEW: whether `cost_center` should be mapped into department semantics or retired later
- REVIEW: whether dept-head document visibility needs additional filters beyond department scoping

## Notes

- 2026-06-15: No destructive database migration, repo split, or infra refactor was performed in this run.
- 2026-06-15: Backend validation is green; remaining major uncertainty is frontend and PostgreSQL validation.
