# Cleanup Report

Last updated: 2026-06-16

## Kept

- Current monorepo application structure
- Current Helm chart
- Current Terraform roots
- Current docs and local development workflow

## Moved

- No physical path moves were executed in this planning pass.

## Merged

- No file merges were executed in this planning pass.

## Deleted

- No files were deleted in this planning pass.

## Manual Review Required

- `infra/k8s/`
- `infra/vm/`
- `infra/vmss/`
- `terraform/azure/vm-docker/`
- `.github/workflows/terraform-dev.yml`
- workspace helper scripts under `terraform/azure/aks/`

## Validation Performed

- Documentation and reference review only for repo/platform planning
- Existing product validation status carried forward from `CURRENT_STATE.md`

## Remaining Cleanup TODOs

- Execute physical split in a tool-complete environment
- Validate new paths and workflows
- Reclassify `REVIEW` items after replacement systems exist
