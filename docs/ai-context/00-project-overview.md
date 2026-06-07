# Project overview

This repository is the deployable monorepo for the Spend Control Platform.

Current deployable units:

- `frontend/`: Next.js finance workspace
- `backend/`: shared FastAPI codebase with four app entrypoints
- `infra/helm/business-ai-app/`: canonical Kubernetes application chart
- `infra/k8s/`: raw manifest mirror
- `terraform/azure/aks/`: Azure, Entra, AKS, Front Door, and Helm bootstrap

Business scope:

- multi-tenant SaaS for both Entra organizations and personal Microsoft account users
- expenses, approvals, budgets, and finance documents
- OCR and invoice extraction
- AI-assisted finance review
