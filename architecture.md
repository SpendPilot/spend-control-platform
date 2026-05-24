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

## Azure Direction

The platform repo now carries two Azure-targeted infrastructure paths:

- `terraform/azure/aks`
- `terraform/azure/vm-docker`

The Terraform is now organized in module style inside each deployment type:

- `terraform/azure/aks/modules/*`
- `terraform/azure/vm-docker/modules/*`

The environment roots are intentionally thin and compose their own custom modules.

### Recommended Edge Pattern

For production on Azure, the cleaner default is:

1. A single public edge gateway
   - path-routes `/` to the frontend
   - path-routes `/api/*` to `control-service`
2. Internal-only service-to-service traffic for `expense-service` and `ai-service`
3. Private PostgreSQL networking

This recommendation matters because the current frontend makes browser-side calls to `control-service`. A strict "frontend public, API private-only" topology would require a frontend proxy/BFF layer first.

### AKS Path

- AKS for long-term scale and cleaner service isolation
- dedicated node pool subnets for system, frontend-oriented workloads, and backend-oriented workloads
- Azure Application Gateway WAF v2 at the edge
- Azure Database for PostgreSQL Flexible Server in a delegated subnet
- Azure Container Registry for Azure-native image delivery

### VM-Docker Path

- one Linux virtual machine for the frontend
- one Linux virtual machine for the backend services
- one Linux virtual machine for PostgreSQL and Ollama
- Azure Application Gateway WAF v2 at the edge with path-based routing
- backend virtual machine intended to host the API tier privately
- PostgreSQL runs inside the data VM as a service
- Azure Container Registry provisioned for later CI/CD hardening

### Why not "public frontend load balancer + internal application gateway" by default

That topology can work, but it is not the best fit for the current app because:

- the browser currently calls the API directly
- a private-only API tier would need frontend proxy rewrites or a BFF layer
- a separate public load balancer plus internal application gateway adds more moving parts without improving the current request path

If you still want that stricter pattern later, the next step is to make the frontend serve API calls on the same origin and proxy them internally.
