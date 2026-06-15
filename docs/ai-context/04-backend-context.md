# Backend context

The backend is a shared FastAPI codebase with multiple entrypoints:

- `app.main:app`
- `app.service_apps.identity:app`
- `app.service_apps.finance:app`
- `app.service_apps.documents:app`

Important modules:

- `app/core/config.py`
- `app/core/security.py`
- `app/core/rbac.py`
- `app/models/__init__.py`
- `app/services/user_service.py`
- `app/services/finance_service.py`
- `app/services/document_service.py`
- `app/services/ai_foundry_service.py`

Key responsibilities:

- validate Entra tokens
- bootstrap organizations from Entra tenant claims or personal-account identities
- persist user sessions
- enforce RBAC
- manage budgets, expenses, approvals, and audit data
- extract OCR text and invoice fields
- analyze documents with Azure AI Foundry
