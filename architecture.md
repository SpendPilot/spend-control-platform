# Spend Control Split-Repo Architecture

## Repositories

The application is now split into separate repo-ready projects:

- `spend-control-frontend`
- `spend-control-control-service`
- `spend-control-expense-service`
- `spend-control-ai-service`
- `spend-control-platform`

## Runtime Topology

1. `spend-control-frontend`
   - Next.js UI on port `3000`
   - calls only `control-service`

2. `spend-control-control-service`
   - public backend on port `8000`
   - auth, RBAC, policies, approvals, dashboards
   - orchestrates `expense-service` and `ai-service`

3. `spend-control-expense-service`
   - domain backend on port `8001`
   - claims, receipts, vendors, budgets, anomalies, audit events

4. `spend-control-ai-service`
   - AI backend on port `8002`
   - Ollama explanations, summaries, and chat

5. Supporting infrastructure
   - PostgreSQL on `5432`
   - Ollama on `11434`

## Deployment Repo Role

`spend-control-platform` is the deployment repo. It contains:

- `docker-compose.yml`
- `k8s/`
- operational docs
- smoke verification script

It assumes the app repos exist as sibling folders in the same parent directory.

