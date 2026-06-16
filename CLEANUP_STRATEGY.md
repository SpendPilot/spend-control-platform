# Cleanup Strategy

Last updated: 2026-06-16

## Principles

- Prefer `REVIEW` over accidental deletion.
- Do not remove stateful or sensitive artifacts automatically.
- Do not delete an old path until its replacement exists and is validated.
- Treat duplicate deployment systems as active risk until one is formally retired.
- Search repository references before changing classification from `REVIEW` to `DELETE`.

## Classification Rules

- `KEEP`: still required in the current monorepo or future split
- `MOVE`: should relocate to a future repo or folder
- `MERGE`: content should be consolidated into another maintained file/folder
- `DELETE`: safe to remove only after replacement and validation
- `REVIEW`: not yet safe to change automatically

## Sensitive Never-Auto-Delete Set

- `terraform.tfstate*`
- real `tfvars` with credentials
- `.env` files with real secrets
- certificates, kubeconfigs, tokens, unknown credential-like material
- production-only scripts or configs whose runtime references are not fully known

## Current High-Risk Cleanup Areas

- `terraform/azure/vm-docker/` because it contains local state files
- `infra/vm/` and `infra/vmss/` because they may still reflect historical deployment paths
- `infra/k8s/` because it overlaps with Helm deployment assets
- `.github/workflows/terraform-dev.yml` because it still points at workspace-based Terraform apply behavior
- root and docs deployment guides that mention the old live workflow

## Execution Rule

No broad deployment cleanup should occur until the target repo layout and target infra layout both exist and their validation steps are either run successfully or explicitly accepted as deferred with owner context.
