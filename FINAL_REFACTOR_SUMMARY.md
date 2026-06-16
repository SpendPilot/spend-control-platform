# Final Refactor Summary

Last updated: 2026-06-16

## What Changed

- Added the missing repo/platform refactor source-of-truth documents required by the `ai-plans`.
- Mapped the current monorepo, service boundaries, split readiness, local-dev expectations, infra target layout, state migration strategy, Helm plan, GitOps plan, CI/CD plan, and cleanup classifications.
- Carried forward the documented validation limitation: PostgreSQL-specific validation is still pending in a suitable environment.

## New Structure Defined

- Future repo split:
  - `spendpilot-frontend`
  - `spendpilot-services`
  - `spendpilot-helm`
  - `spendpilot-infra`
  - `spendpilot-gitops`
  - `spendpilot-docs`
- Future infra split:
  - shared/global roots
  - env-specific Terraform roots
  - Helm/GitOps separation from Terraform service deployment

## Infrastructure Changes

- Planning/docs only in this pass
- no live Terraform state migration
- no apply operations

## Helm Changes

- Refactor plan documented for moving the current chart into a standalone Helm repo shape

## GitOps Changes

- ArgoCD environment layout and promotion/rollback strategy documented

## CI/CD Changes

- Target OIDC-based, path-filtered workflow strategy documented
- current workspace-based Terraform workflow flagged for later replacement

## Deleted Files/Folders

- None in this pass

## Remaining Manual Review Items

- `infra/k8s/`
- `infra/vm/`
- `infra/vmss/`
- `terraform/azure/vm-docker/`
- `.github/workflows/terraform-dev.yml`
- workspace helper scripts and old deployment docs

## Validation Status

- Product validation carried forward from existing context
- Repo/platform/infrastructure work in this pass is planning/documentation-only
- cloud/tooling-dependent validations remain pending

## Known Risks

- PostgreSQL migration validation still pending
- current Terraform workspace flow conflicts with target env-root state strategy
- overlapping deployment systems remain until later cleanup

## Next Steps

1. Run the physical repo split in a fully tooled environment.
2. Build the target infra repo layout and migrate Terraform state carefully.
3. Move the chart and create GitOps desired state.
4. Replace the old workflow and deployment paths only after validation.
