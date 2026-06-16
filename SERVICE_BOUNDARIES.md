# Service Boundaries

Last updated: 2026-06-16

## Proposed Services

### `spendpilot-frontend`

Owns:
- Next.js UI
- role-aware navigation and onboarding routes
- charts, forms, tenant-scoped client interactions

Current source:
- `frontend/`

Future repo:
- `repos/spendpilot-frontend/`

### `identity-service`

Owns:
- authentication integration
- current-user resolution
- tenant bootstrap
- organization memberships
- role and department assignment admin actions

Current source:
- `backend/app/service_apps/identity.py`
- `backend/app/api/routes/auth.py`
- `backend/app/api/routes/admin.py`
- auth and RBAC helpers in `backend/app/core/`
- membership/user flows in `backend/app/services/user_service.py`

Future repo grouping:
- `repos/spendpilot-services/services/identity-service/`

### `finance-service`

Owns:
- budgets
- recurring expenses
- recurring expense requests
- variable expenses
- approvals
- spend limits
- payment priority and cash outflow logic

Current source:
- `backend/app/service_apps/finance.py`
- `backend/app/api/routes/finance.py`
- `backend/app/services/finance_service.py`
- finance schemas and related models

Future repo grouping:
- `repos/spendpilot-services/services/finance-service/`

### `documents-service`

Owns:
- bill upload
- storage integration
- extraction orchestration
- bills library data
- document to expense linking

Current source:
- `backend/app/service_apps/documents.py`
- `backend/app/api/routes/documents.py`
- `backend/app/services/document_service.py`
- `backend/app/services/storage_service.py`

Future repo grouping:
- `repos/spendpilot-services/services/documents-service/`

### `ai-service` logical boundary

Owns:
- AI chat prompt/context assembly
- tenant-grounded financial insights
- AI Foundry/OpenAI integration logic

Current source:
- `backend/app/api/routes/ai.py`
- `backend/app/services/ai_chat_service.py`
- `backend/app/services/ai_foundry_service.py`

Near-term recommendation:
- keep colocated with backend services repo, most likely under `finance-service` plus a small `ai/` internal package

## Shared Technical Libraries

Allowed shared areas in future `repos/spendpilot-services/libs/`:

- `common/`: shared exceptions, base DTO helpers only if genuinely cross-service
- `config/`: env/config loading
- `auth/`: token validation and shared access helpers
- `observability/`: logging, tracing, metrics helpers

Business ownership should remain in service folders, not shared libs.

## Database Ownership

- Single shared PostgreSQL database today
- Logical ownership:
  - identity: tenants, users, memberships, departments
  - finance: budgets, expenses, approvals, spend limits, payment priorities, vendors
  - documents: documents, extractions, storage references
  - ai: chat sessions/messages, grounded insight traces if stored

## Current Coupling

- Shared SQLAlchemy models and shared session lifecycle
- Shared FastAPI project with multiple app entrypoints
- Finance and documents intersect around bill-linked expenses
- Identity intersects with every service through membership and tenant scoping

## Future Split Strategy

1. Split repo boundaries first while keeping a shared deployment contract.
2. Keep one services repo initially.
3. Isolate technical shared libraries.
4. Only split into separate service repos once API contracts, database ownership, and CI pipelines are stable.
