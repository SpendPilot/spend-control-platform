# Decisions

Last updated: 2026-06-16

## 2026-06-15 - D-001 - Use repo-level handoff docs plus existing `docs/ai-context/`

Status: Accepted

Decision:
- Keep detailed historical/runtime context in `docs/ai-context/`.
- Add repo-root handoff and phase-tracking docs for the current refactor run.

## 2026-06-15 - D-002 - Keep membership-scoped roles and departments

Status: Accepted

Decision:
- Keep department assignment and onboarding state on `organization_memberships`, not on the global `users` table.
- Keep `platform_admin` as a separate global capability on `users.platform_role`.

## 2026-06-15 - D-003 - Canonicalize product roles without discarding compatibility

Status: Accepted

Decision:
- Canonical membership roles are now `org_owner`, `dept_head`, and `employee`.
- Legacy role names remain accepted as aliases during transition.

## 2026-06-15 - D-004 - Reuse the existing `expenses` and `documents` tables as the variable-expense and bills baseline

Status: Accepted

Decision:
- Extend `expenses` to carry the variable-expense workflow.
- Extend `documents` to carry the bills-library workflow.
- Add recurring-expense, spend-limit, payment-priority, vendor, and AI-chat tables additively.

## 2026-06-15 - D-005 - Ship a functional role-aware frontend baseline before a full UX polish pass

Status: Accepted

Decision:
- Implement the target product pages and role-aware navigation as a working baseline now.
- Defer final UX polish and full compiler validation until Node tooling is available.

## 2026-06-16 - D-006 - Keep additive migrations SQLite-compatible for local validation

Status: Accepted

Decision:
- Update altered-table Alembic migrations to use batch operations where foreign keys and indexes are added to existing tables.
- Preserve the additive schema shape while allowing local SQLite upgrade validation to succeed alongside PostgreSQL rollout planning.

## 2026-06-16 - D-007 - Prefer locally buildable frontend validation inputs

Status: Accepted

Decision:
- Remove runtime dependence on Google-hosted `next/font/google` downloads during local builds.
- Pin frontend TypeScript to `5.6.3` for stable Next 14 validation in this repo.
- Repair the local `next` install instead of introducing custom ambient type shims.

## 2026-06-16 - D-008 - Allow repo/platform restructure to proceed despite the remaining PostgreSQL validation gap

Status: Accepted

Decision:
- Treat the missing PostgreSQL Alembic validation as an environment limitation on the user's company-managed laptop, not as a silent success.
- Proceed with the repo/application/infrastructure planning and restructure workflow only because the user explicitly approved skipping that validation-only blocker for now.

Impact:
- Repo/platform restructure work can continue in this machine environment.
- PostgreSQL validation remains a required follow-up before production rollout.

Future change option:
- Once a PostgreSQL runtime is available, rerun the Alembic validation and then downgrade this exception back to normal completed validation status.

## 2026-06-16 - D-009 - Complete the ai-plan deliverables as planning and handoff documentation before physical execution

Status: Accepted

Decision:
- Create the missing repo split and platform refactor source-of-truth files now.
- Treat the later `ai-plans` as complete for planning/documentation deliverables, not as proof that the physical split or infra migration already happened.

Impact:
- Future agents now have a consistent plan of record for repo split, infra migration, cleanup, and validation sequencing.
- The current monorepo remains the live working structure until execution happens in a fully equipped environment.
