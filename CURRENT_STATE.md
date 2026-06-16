# Current State

Last updated: 2026-06-16

## Scope Of This Run

- Active scope in this continued run: progressed from Phase `-1` through the remaining product-refactor phases with honest `COMPLETE` vs `PARTIAL` status tracking.
- Active scope in the latest continuation: complete the missing repo/platform refactor planning deliverables referenced by the `ai-plans`.
- Still explicitly out of scope:
  - physical repo split execution
  - live CI/CD workflow replacement
  - live Terraform / Helm / GitOps restructuring
  - destructive cleanup deletions

## Repository Shape Confirmed

- The repo remains a single monorepo with `frontend/`, `backend/`, `infra/`, `terraform/`, `docs/`, `scripts/`, and `data/`.
- No repo split was performed in this run.
- All product refactor work was kept compatible with later repo/platform refactor prompts.

## Current Product Baseline

- Auth: Microsoft Entra production path plus `dev-local`
- Tenant bootstrap: first authenticated membership becomes `org_owner`
- Roles: `org_owner`, `dept_head`, `employee`
- Departments: `IT`, `Marketing`, `HR`
- Finance: budgets, variable expenses, recurring expenses, recurring requests, spend limits, payment priorities
- Documents: upload, scan, extraction, expense linking, bills-library baseline
- AI: tenant-scoped chat sessions and grounded finance responses
- Audit: audit-event capture remains active

## Phase Status

- Phase -1: COMPLETE
- Phase 0: COMPLETE
- Phase 1: COMPLETE
- Phase 2: COMPLETE
- Phase 3: COMPLETE
- Phase 4: COMPLETE
- Phase 5: COMPLETE
- Phase 6: COMPLETE
- Phase 7: COMPLETE
- Phase 8: COMPLETE
- Phase 9: COMPLETE
- Phase 10: COMPLETE
- Phase 11: COMPLETE
- Phase 12: PARTIAL
- Phase 13: COMPLETE

## What "Partial" Means Here

- The only remaining incomplete phase is Phase 12.
- Product workflows and frontend validation are now complete in this environment.
- PostgreSQL-specific migration validation still requires a runnable PostgreSQL environment.
- 2026-06-16: The user explicitly approved moving on to the repo/platform restructure plans even though PostgreSQL validation cannot be completed on this company-managed laptop.

## Validation State

- Backend tests: PASS (`pytest` in `backend/`)
- Alembic upgrade on SQLite validation database: PASS after making Phase 1 and Phase 2 migrations SQLite-safe for altered tables
- Frontend typecheck: PASS (`node ./node_modules/typescript/bin/tsc --noEmit` in `frontend/`)
- Frontend lint: PASS (`npm run lint` in `frontend/`)
- Frontend build: PASS (`npm run build` in `frontend/`)
- PostgreSQL migration dry run: NOT VALIDATED in this environment
- Post-phase cleanup pass: COMPLETE for safe non-destructive fixes; no safe file deletions were identified in this run

## Key Files Added Or Expanded In Later Phases

- Backend:
  - `backend/app/models/__init__.py`
  - `backend/app/schemas/ai.py`
  - `backend/app/schemas/finance.py`
  - `backend/app/services/finance_service.py`
  - `backend/app/services/ai_chat_service.py`
  - `backend/app/services/document_service.py`
  - `backend/app/api/routes/finance.py`
  - `backend/app/api/routes/ai.py`
  - `backend/app/db/migrations/versions/20260615_0003_payment_ops_core.py`
  - `backend/tests/test_finance.py`
  - `backend/tests/test_ai_chat.py`
- Frontend:
  - `frontend/components/app-shell.tsx`
  - `frontend/app/dashboard/page.tsx`
  - `frontend/app/expenses/page.tsx`
  - `frontend/app/budgets/page.tsx`
  - `frontend/app/documents/page.tsx`
  - `frontend/app/settings/page.tsx`
  - `frontend/app/approvals/page.tsx`
  - `frontend/app/spend-limits/page.tsx`
  - `frontend/app/payment-priority/page.tsx`
  - `frontend/app/ai-insights/page.tsx`
  - `frontend/app/profile/page.tsx`
  - `frontend/app/scan/page.tsx`

## Notes

- 2026-06-15: The codebase now represents a functional payment-operations baseline inside the original unsplit SpendPilot repo.
- 2026-06-15: The main remaining execution risk is now PostgreSQL rollout validation, not frontend or backend correctness.
- 2026-06-15: Follow-up cleanup removed stale user-facing role wording in deployment docs and fixed mojibake in the settings page without changing product behavior.
- 2026-06-16: Validation rerun confirmed backend tests still pass and exposed a real frontend package-lock/install issue rather than a missing Node runtime.
- 2026-06-16: Alembic migrations `20260615_0002` and `20260615_0003` were updated to use batch table rewrites for altered tables so local SQLite validation succeeds.
- 2026-06-16: Frontend validation now passes after repairing the local Next install, pinning TypeScript to `5.6.3`, and removing runtime dependence on Google-hosted font downloads during build.
- 2026-06-16: Org-owner recurring-request review, department reassignment, and bill-linked expense submission are now exposed directly in the frontend workflows.
- 2026-06-16: Repo/platform restructure work may proceed as a user-approved exception despite the remaining PostgreSQL validation gap; that gap must stay documented in risks and handoff notes.
- 2026-06-16: Added the missing repo/platform planning docs required by later `ai-plans`, including repo split, service boundary, infra, Helm, GitOps, CI/CD, and cleanup source-of-truth files.
- 2026-06-16: Those later phases are complete as documentation and handoff work, but physical code moves, Terraform state migration, workflow replacement, and destructive cleanup were intentionally deferred.
