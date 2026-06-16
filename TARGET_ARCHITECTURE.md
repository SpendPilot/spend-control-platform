# Target Architecture

Last updated: 2026-06-16

## Repository Target

Planned future split from the current monorepo:

```txt
repos/
  spendpilot-frontend/
  spendpilot-services/
  spendpilot-helm/
  spendpilot-infra/
  spendpilot-gitops/
  spendpilot-docs/
```

The current repository remains the working source until each target area is validated in isolation.

## Application Runtime Target

```txt
Azure Front Door
  -> kGateway on AKS
  -> HTTPRoutes
      -> frontend
      -> identity service
      -> finance service
      -> documents service
  -> PostgreSQL Flexible Server
  -> Azure Blob Storage
  -> Azure AI Foundry / OpenAI
  -> Azure AI Document Intelligence
```

## Service Target

- `frontend`: Next.js tenant-aware UI
- `identity-service`: auth, tenant bootstrap, role and membership management
- `finance-service`: budgets, expenses, approvals, spend limits, payment priority
- `documents-service`: upload, OCR, extraction, bill-library workflows
- `shared libs`: technical helpers only, not domain ownership

## Platform Target

- `spendpilot-infra`
  - Terraform modules
  - separate root modules per state
  - Azure Blob backend
  - no Terraform workspaces for environment separation
- `spendpilot-helm`
  - one umbrella chart first
  - env override values files
- `spendpilot-gitops`
  - ArgoCD desired state per environment
- `GitHub Actions`
  - OIDC to Azure where possible
  - path-filtered workflows
  - immutable image tags

## Environment Target

- `global-shared`: ACR and truly global identities or shared resources
- `nonprod-shared`: Front Door and optional shared AI services for dev/staging
- `dev`: full runtime state
- `staging`: full runtime state
- `prod`: full runtime plus prod Front Door and tighter security controls

## Guiding Rules

- Application deployment belongs to Helm/GitOps, not Terraform service resources.
- No two Terraform states may manage the same Azure resource.
- Shared resources must have their own state.
- Prod remains public AKS for now, with documented hardening and future private-cluster migration.
