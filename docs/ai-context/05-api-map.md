# API map

Shared health:

- `GET /health`
- `GET /ready`

Identity service:

- `GET /api/auth/me`
- `POST /api/auth/dev-login`
- `GET /api/admin/organization`
- `GET /api/admin/members`
- `PATCH /api/admin/members/{membership_id}`
- `GET /api/admin/sessions`
- `POST /api/admin/sessions/{session_id}/revoke`

Finance service:

- `GET /api/finance/dashboard`
- `GET /api/finance/categories`
- `GET /api/finance/budgets`
- `POST /api/finance/budgets`
- `GET /api/finance/expenses`
- `POST /api/finance/expenses`
- `GET /api/finance/expenses/{expense_id}`
- `POST /api/finance/expenses/{expense_id}/approve`
- `POST /api/finance/expenses/{expense_id}/reject`

Documents service:

- `GET /api/documents`
- `POST /api/documents/upload`
- `GET /api/documents/{id}`
- `POST /api/documents/{id}/scan`
- `GET /api/documents/{id}/scan-result`
- `POST /api/documents/{id}/extract-expense`
- `POST /api/ai/analyze`
