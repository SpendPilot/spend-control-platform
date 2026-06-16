# Local Development

Last updated: 2026-06-16

## Current Monorepo Workflow

### Run everything with Docker Compose

```bash
docker compose up --build
```

Services started:

- PostgreSQL
- backend combined API
- frontend

### Frontend only

```bash
cd frontend
npm install
npm run lint
node ./node_modules/typescript/bin/tsc --noEmit
npm run build
```

### Backend only

```bash
cd backend
pytest
```

## Required Environment

Core local env is driven by `.env` plus the example files:

- `.env.example`
- `frontend/.env.example`
- Azure/VM examples if needed for historical deployment paths

Important local settings:

- `AUTH_MODE=dev-local`
- `NEXT_PUBLIC_AUTH_MODE=dev-local`
- `DATABASE_URL`
- Azure AI, storage, and extraction env vars only if testing those integrations

## Local Dependencies

- Node/npm for frontend
- Python for backend
- Docker Desktop or equivalent for compose workflow
- PostgreSQL if validating outside Docker

## Known Validation Limits On This Laptop

- PostgreSQL migration validation was not completed locally.
- Terraform/Helm/GitOps tooling is not assumed to be installed here.
- Cloud-facing validation should be run later in an equipped environment.

## Future Split Workflow

After repo split:

- `spendpilot-frontend` should run independently against deployed or local service endpoints
- `spendpilot-services` should expose local service entrypoints and shared compose helpers
- `spendpilot-helm`, `spendpilot-infra`, and `spendpilot-gitops` should validate independently

## Troubleshooting

- If frontend build fails, verify `frontend/package-lock.json` and local Next/TypeScript install consistency.
- If backend tests fail on schema changes, rerun migration validation in a PostgreSQL-capable environment.
- If auth appears broken locally, confirm both frontend and backend are using `dev-local`.
