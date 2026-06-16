# AI Context

Last updated: 2026-06-16

## Purpose

This file is the repo-level entrypoint for the post-product-refactor planning phases. It summarizes the current monorepo shape, the intended repository/platform split, and the constraints future agents must preserve while finishing repo, infra, Helm, GitOps, and CI/CD work.

## Current Reality

- This is still the original unsplit `SpendPilot` repository.
- Product refactor phases are functionally complete except for PostgreSQL-specific validation that could not be run on this company-managed laptop.
- The repo currently contains both application code and deployment/platform code:
  - `frontend/`
  - `backend/`
  - `infra/`
  - `terraform/`
  - `.github/`
  - `docs/`
- The current canonical Kubernetes application packaging is `infra/helm/business-ai-app/`.
- The current canonical Azure provisioning path is `terraform/azure/aks/`.
- Legacy or overlapping deployment shapes still exist and must be treated carefully:
  - `infra/k8s/` raw manifests
  - `infra/vm/`
  - `infra/vmss/`
  - `terraform/azure/vm-docker/`

## Source Of Truth

- Current implementation state: `CURRENT_STATE.md`
- Target architecture direction: `TARGET_ARCHITECTURE.md`
- Phase and migration planning: `REFACTOR_PLAN.md`, `MIGRATION_CHECKLIST.md`
- Decisions: `DECISIONS.md`
- Risks: `RISK_REGISTER.md`
- Cleanup policy: `CLEANUP_STRATEGY.md`, `CLEANUP_PLAN.md`, `CLEANUP_INFRA_DEPLOYMENT_PLAN.md`
- Service decomposition planning: `SERVICE_BOUNDARIES.md`, `SERVICE_SPLIT_READINESS.md`, `REPO_SPLIT_PLAN.md`
- Infra/platform planning: `INFRA_REFACTOR_PLAN.md`, `STATE_MIGRATION_PLAN.md`, `SHARED_RESOURCE_STRATEGY.md`, `FRONTDOOR_ORIGIN_STRATEGY.md`, `SECURITY_BASELINE.md`, `HELM_REFACTOR_PLAN.md`, `GITOPS_STRATEGY.md`, `CICD_STRATEGY.md`

## Constraints

- Do not delete Terraform state files, secrets, certificates, kubeconfigs, or unknown production files automatically.
- Do not run destructive database migrations or destructive Terraform state commands without explicit approval.
- Do not leave two active deployment systems unmanaged by documentation.
- Keep the current monorepo runnable until physical split work is validated elsewhere.
- Treat unavailable local tooling as a validation constraint, not as implied success.

## Current Outcome Of This Planning Pass

- The repo/application/infrastructure split strategy is now documented.
- Cleanup candidates and high-risk areas are classified.
- Validation gaps are explicitly recorded.
- Physical repo split, cloud-state migration, and full platform rollout remain planned follow-up work.
