# State Migration Plan

Last updated: 2026-06-16

## Current State Situation

- `terraform/azure/aks/` is documented and automated around a live `dev` workspace flow.
- `.github/workflows/terraform-dev.yml` performs `terraform workspace select dev` and applies from that root.
- `terraform/azure/vm-docker/` contains local `terraform.tfstate` and `terraform.tfstate.backup` files that must not be deleted automatically.

## Target State Files

- `global-shared.tfstate`
- `nonprod-shared.tfstate`
- `dev.tfstate`
- `staging.tfstate`
- `prod.tfstate`

## Backend Configuration Strategy

- keep Azure Blob backend
- create explicit backend config per env root
- avoid workspace-based environment switching

## State Backup Steps

1. Export or copy remote state for the current AKS root before any move.
2. Preserve local backup copies of any state touched during migration.
3. Snapshot relevant resource inventories before changing state ownership.

## Migration Steps

1. Inventory resources currently managed by `terraform/azure/aks/`.
2. Map each resource to target ownership: `global-shared`, `nonprod-shared`, `dev`, `staging`, or `prod`.
3. Create target env roots and modules.
4. Initialize new backends without apply.
5. Move/import state carefully into the correct target roots.
6. Run plans to confirm no duplicate creation/destruction.
7. Retire workspace-based automation only after new plans are stable.

## `terraform state mv` / `import` Guidance

- Use `terraform state mv` only when source and destination state ownership are fully mapped.
- Use `terraform import` when resources must be attached to a newly created root state.
- Never run bulk or destructive state commands automatically.

## Rollback Notes

- Keep old state snapshots until all new roots plan cleanly.
- If duplicate ownership appears, revert to the last known good backed-up state mapping and reassess.

## Manual Review Warnings

- verify whether any shared Azure resources are still co-owned across AKS and VM/docker Terraform roots
- verify whether Helm bootstrap resources are currently being managed indirectly from Terraform

## Warning

Destructive state commands must not run automatically without explicit approval.
