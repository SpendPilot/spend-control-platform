# Final Operations Guide

Last updated: 2026-06-15

## Backend Validation

Run from `backend/`:

```powershell
pytest
```

## Frontend Validation

When Node tooling is available, run from `frontend/`:

```powershell
npm run build
npm run lint
```

## Migration Validation

When validating against a real database:

```powershell
alembic upgrade head
```

## Safety Notes

- keep `dev-local` auth only for local development and tests
- do not run destructive migrations automatically
- do not mix product refactor work with repo split or infra refactor work in the same pass
