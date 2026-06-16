# Final Folder Structure

Last updated: 2026-06-16

## Current Working Structure

```txt
frontend/        application UI
backend/         shared backend codebase with service entrypoints
infra/           helm, raw k8s, and historical VM/VMSS deployment assets
terraform/       current AKS and legacy VM/docker Terraform roots
docs/            architecture, deployment, and AI context docs
.github/         current workflows
scripts/         helper scripts
data/            local data artifacts
```

## Future Standalone Repos

- `spendpilot-frontend`
- `spendpilot-services`
- `spendpilot-helm`
- `spendpilot-infra`
- `spendpilot-gitops`
- `spendpilot-docs`

## Required Folders

- current `frontend/`, `backend/`, `infra/helm/business-ai-app/`, `terraform/azure/aks/`, and `docs/` remain required until the split is executed and validated

## Old Structures Not Yet Removed

- `infra/k8s/`
- `infra/vm/`
- `infra/vmss/`
- `terraform/azure/vm-docker/`
- workspace-based Terraform helper flow

These remain because safe replacement validation has not yet happened.
