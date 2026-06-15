# Product Refocus Plan

Last updated: 2026-06-15

## Goal

Refocus the current finance workspace into a centralized business payment operations platform while preserving:

- authentication
- tenant isolation
- first-user bootstrap behavior
- document upload and extraction
- current deployable monorepo structure

## Current To Target Mapping

| Current capability | Reuse plan | Target direction |
| --- | --- | --- |
| Organization bootstrap and memberships | Preserve | Use as the tenant-scoped identity base for `org_owner`, `dept_head`, `employee` |
| Budgets | Reuse and extend | Company and department budget views |
| Expenses | Reuse and split conceptually | Separate recurring and variable expense flows |
| Expense approvals | Reuse and refactor | Employee -> dept_head -> org_owner approval path |
| Document upload and extraction | Preserve | Bill library and bill-linked expense workflow |
| AI document analysis | Preserve | Later AI insights and finance assistant grounding |
| Audit events | Preserve | Track role, department, and approval changes |

## Phase 1 Refocus

- Introduce default departments: `IT`, `Marketing`, `HR`
- Move role semantics toward:
  - `org_owner`
  - `dept_head`
  - `employee`
- Require employees to finish department onboarding before using employee flows
- Add org-owner user-management controls needed for later feature phases

## Explicit Non-Goals In This Run

- No repo split
- No infra restructuring
- No full recurring-expense feature build
- No AI insights chatbot build
- No product cleanup deletions

## Compatibility Rule

All Phase 1 changes must stay compatible with the current frontend/backend monorepo and with later repo/platform refactor prompts.
