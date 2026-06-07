# Spend Control Platform

Spend Control Platform is a multi-tenant business finance management application built for Microsoft Entra ID, Azure AI, and AKS.

Current target runtime:

```txt
User
  -> Azure Front Door Premium + WAF
  -> HTTPS origin to kGateway on AKS
  -> HTTPRoutes
      -> frontend
      -> identity-service
      -> finance-service
      -> documents-service
  -> PostgreSQL Flexible Server (General Purpose, zone-redundant HA, geo-backup)
  -> Azure Blob Storage
  -> Azure AI Foundry
  -> Azure AI Document Intelligence
```

## What is included

- Multi-tenant organization model for both Entra workforce tenants and personal Microsoft accounts
- Session-aware Entra auth with dev-only local fallback
- Finance domain for budgets, expenses, approvals, documents, and audit events
- Invoice and receipt extraction with Document Intelligence
- AI policy/risk summaries with Azure AI Foundry plus local fallback behavior
- AKS deployment assets using Gateway API and kGateway
- Terraform stack that bootstraps Azure, AKS, Entra app registrations, workload identity, Helm releases, and Front Door
- Front Door edge hardening with HTTPS origin forwarding and auth rate limiting at WAF

## Repository layout

```txt
frontend/                     Next.js application
backend/                      FastAPI shared code + split service entrypoints
infra/helm/business-ai-app/   Helm chart for frontend + 3 backend services
infra/k8s/                    Raw Gateway API manifests
terraform/azure/aks/          Azure + AKS + Front Door bootstrap
docs/                         Architecture, deployment, and AI context
```

## Backend runtime shape

- `app.main:app`: combined API for local development
- `app.service_apps.identity:app`: auth, organization, session, and admin routes
- `app.service_apps.finance:app`: budgets, dashboard, expenses, approvals
- `app.service_apps.documents:app`: documents, scans, OCR, and AI analysis

## Local development

1. Copy `.env.example` to `.env`.
2. Keep local auth enabled:
   - `AUTH_MODE=dev-local`
   - `NEXT_PUBLIC_AUTH_MODE=dev-local`
3. Start the stack:

```bash
docker compose up --build
```

Useful local checks:

```bash
cd backend && pytest
helm template spend-control infra/helm/business-ai-app
```

## Deployment references

- [Architecture](docs/azure-infrastructure.md)
- [AKS + Front Door + kGateway](docs/deployment/aks-kgateway-frontdoor.md)
- [Terraform AKS runbook](docs/deployment/terraform-aks-runbook.md)
- [Azure portal manual setup](docs/deployment/azure-portal-manual-setup.md)
- [AKS Helm deployment](docs/deployment/aks-helm.md)
- [AKS raw manifests](docs/deployment/aks-raw-yaml.md)
- [Entra app setup](docs/deployment/azure-entra-setup.md)
- [Managed identity and workload identity](docs/deployment/azure-managed-identity-setup.md)
- [Azure AI Foundry and Document Intelligence](docs/deployment/azure-ai-foundry-setup.md)
- [Environment variables](docs/deployment/environment-variables.md)

Authentication note:

- Work or school accounts are grouped by their Entra tenant ID.
- Personal Microsoft accounts that sign in directly through the Microsoft consumer tenant get their own isolated workspace.
- Guest Microsoft accounts invited into a company Entra tenant stay inside that tenant workspace instead of creating a second personal workspace.
- The frontend must request the API scope using the backend Application ID URI, not the backend client ID.

Current validated Azure posture:

- Front Door forwards to the AKS gateway over `HTTPS`, not `HTTP`.
- The gateway `LoadBalancer` service exposes both `80` and `443`, with the HTTPS listener terminated by a Terraform-managed origin certificate secret.
- PostgreSQL now runs as `GP_Standard_D2s_v3` in `Central India` with `ZoneRedundant` HA and geo-redundant backup enabled.
- Blob Storage defaults the account to OAuth auth for the application path, while shared-key auth remains enabled only so the current AzureRM/Terraform path can keep managing the account safely.

## AI context

Agent-facing repository context lives in `docs/ai-context/`.
