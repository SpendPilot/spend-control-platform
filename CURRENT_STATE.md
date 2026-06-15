# Current State

Last updated: 2026-06-15

## Scope Of This Run

- Active scope in this continued run: progressed from Phase `-1` through the remaining product-refactor phases with honest `COMPLETE` vs `PARTIAL` status tracking.
- Still explicitly out of scope:
  - repo split
  - CI/CD refactor
  - Terraform / Helm / GitOps restructuring
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
- Phase 4: PARTIAL but functional
- Phase 5: PARTIAL but functional
- Phase 6: PARTIAL but functional
- Phase 7: PARTIAL but functional
- Phase 8: PARTIAL but functional
- Phase 9: COMPLETE
- Phase 10: COMPLETE
- Phase 11: PARTIAL
- Phase 12: PARTIAL
- Phase 13: COMPLETE

## What "Partial" Means Here

- The backend and route surface for the requested workflows now exists.
- The frontend exposes the new product areas and role-aware navigation.
- Some UX details still need iteration and full frontend compiler/build validation.

## Validation State

- Backend tests: PASS (`pytest` in `backend/`)
- Frontend build: NOT VALIDATED locally because `node`, `npm`, and `pnpm` are unavailable in the current shell environment
- Frontend lint/typecheck: NOT VALIDATED locally for the same reason
- PostgreSQL migration dry run: NOT VALIDATED in this environment
- Post-phase cleanup pass: COMPLETE for safe non-destructive fixes (frontend text cleanup, finance route import cleanup, Entra role terminology update)

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
- 2026-06-15: The main remaining execution risk is frontend build/type validation, not backend correctness.
- 2026-06-15: Follow-up cleanup removed stale user-facing role wording in deployment docs and fixed mojibake in the settings page without changing product behavior.
