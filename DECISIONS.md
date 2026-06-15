# Decisions

Last updated: 2026-06-15

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
