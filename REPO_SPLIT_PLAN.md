# Repo Split Plan

Last updated: 2026-06-16

## Current Monorepo Layout

```txt
frontend/
backend/
infra/
terraform/
docs/
.github/
scripts/
data/
```

## Target Repo Layout

```txt
repos/
  spendpilot-frontend/
  spendpilot-services/
  spendpilot-helm/
  spendpilot-infra/
  spendpilot-gitops/
  spendpilot-docs/
```

## What Moves Where

- `frontend/` -> `repos/spendpilot-frontend/`
- `backend/` -> `repos/spendpilot-services/`
- `docs/` plus selected root docs -> `repos/spendpilot-docs/`
- `infra/helm/business-ai-app/` -> `repos/spendpilot-helm/charts/spendpilot/`
- `terraform/` and selected infra bootstrap docs -> `repos/spendpilot-infra/`
- future ArgoCD desired-state files -> `repos/spendpilot-gitops/`

## What Stays Temporarily

- Root-level context and handoff docs until split is validated
- `docker-compose.yml` until frontend/services split has a replacement local-dev path
- historical deployment paths marked for review

## Repo-Ready Areas Today

- `frontend/`
- `backend/`
- `infra/helm/business-ai-app/`
- most of `docs/ai-context/` and `docs/deployment/`

## Monorepo Assumptions Still Present

- root compose workflow
- root environment expectations
- shared backend packaging under one Python project
- workflow and deployment references pointing into current paths

## Suggested Split Order

1. `spendpilot-docs`
2. `spendpilot-frontend`
3. `spendpilot-services`
4. `spendpilot-helm`
5. `spendpilot-infra`
6. `spendpilot-gitops`

## Future Remote Names

- `spendpilot-frontend`
- `spendpilot-services`
- `spendpilot-helm`
- `spendpilot-infra`
- `spendpilot-gitops`
- `spendpilot-docs`

## Deletion Rule

Do not delete the old monorepo paths until each moved area builds, tests, and has no active references from workflows, compose, Terraform, Helm, scripts, or docs.
