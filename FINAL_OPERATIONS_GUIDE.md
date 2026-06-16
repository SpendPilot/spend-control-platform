# Final Operations Guide

Last updated: 2026-06-16

## Backend Validation

Run from `backend/`:

```powershell
pytest
```

## Frontend Validation

Run from `frontend/`:

```powershell
npm install
npx tsc --noEmit
npm run build
npm run lint
```

## Migration Validation

SQLite validation used in this run:

```powershell
$env:DATABASE_URL='sqlite:///./tests/alembic-validation.db'
alembic upgrade head
```

PostgreSQL validation still needs a real PostgreSQL runtime. When available, run from `backend/`:

```powershell
$env:DATABASE_URL='postgresql+psycopg://<user>:<password>@<host>:5432/<db>'
alembic upgrade head
```

## Safety Notes

- keep `dev-local` auth only for local development and tests
- do not run destructive migrations automatically
- do not mix product refactor work with repo split or infra refactor work in the same pass
- this repo is ready for later repo split / CI-CD / infra refactor prompts after PostgreSQL migration validation
