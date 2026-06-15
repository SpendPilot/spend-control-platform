# Data Model Changelog

Last updated: 2026-06-15

## Added In Phase 1

- `departments`
- `organization_memberships.department_id`
- `organization_memberships.onboarding_completed`

## Added In Later Phases

- `vendors`
- `recurring_expenses`
- `recurring_expense_requests`
- `spend_limits`
- `payment_priorities`
- `ai_chat_sessions`
- `ai_chat_messages`

## Extended Existing Tables

- `budgets`
  - `department_id`
  - `scope`
  - `month`
  - `year`
- `expenses`
  - `department_id`
  - `vendor_id`
  - `expense_type`
  - `dept_head_reviewer_user_id`
  - `org_owner_approver_user_id`
  - `rejection_reason`
  - `payment_status`
- `documents`
  - `department_id`
  - `linked_expense_type`
  - `linked_expense_id`

## Safety Notes

- All schema changes in this run were additive.
- No destructive migration was executed automatically.
