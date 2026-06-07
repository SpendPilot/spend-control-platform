# Database context

Primary schema now includes:

- `organizations`
- `users`
- `organization_memberships`
- `user_sessions`
- `expense_categories`
- `budgets`
- `expenses`
- `expense_approvals`
- `documents`
- `document_scans`
- `audit_events`

Database expectations:

- SQLite stays acceptable for tests
- PostgreSQL Flexible Server is the intended Azure runtime
- one logical database serves all three backend services
