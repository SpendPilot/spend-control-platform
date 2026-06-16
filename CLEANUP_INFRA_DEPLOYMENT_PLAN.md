# Cleanup Infra Deployment Plan

Last updated: 2026-06-16

| Path | Classification | Reason | Replacement path | References found | Safe to remove now | Validation required |
| --- | --- | --- | --- | --- | --- | --- |
| `terraform/azure/aks/` | MOVE | current active AKS root should become env-root infra repo source | `repos/spendpilot-infra/envs/*` and `modules/` | root README, docs, workflow | no | terraform validate/plan in new structure |
| `terraform/azure/aks/dev-workspace.ps1` | DELETE | conflicts with no-workspace target strategy | env-root init/apply docs | root README and workflow behavior | no | workspace replacement validated |
| `.github/workflows/terraform-dev.yml` | REVIEW | directly applies workspace-based Terraform | future environment-aware infra workflows | root README, docs | no | new workflows validated |
| `terraform/azure/vm-docker/` | REVIEW | legacy infra path and contains local state files | none yet | docs and infra history | no | confirm no active ownership |
| `terraform/azure/vm-docker/terraform.tfstate` | KEEP | state file must never be auto-deleted | n/a | local terraform path only | no | manual review only |
| `terraform/azure/vm-docker/terraform.tfstate.backup` | KEEP | state backup must never be auto-deleted | n/a | local terraform path only | no | manual review only |
| `infra/helm/business-ai-app/` | MOVE | future standalone Helm repo chart | `repos/spendpilot-helm/charts/spendpilot/` | README, docs, workflow, terraform refs | no | helm lint/template in new location |
| `infra/k8s/` | REVIEW | raw manifests overlap with Helm/GitOps target | chart + gitops manifests | README and deployment docs | no | confirm no fallback need remains |
| `infra/vendor/kgateway/` | REVIEW | may remain vendored or be replaced by bootstrap module/external source | target infra/helm bootstrap path | chart/manual refs | no | decide bootstrap approach |
| `infra/vm/` | REVIEW | legacy VM deployment path | none yet | docs and scripts | no | confirm retired |
| `infra/vmss/` | REVIEW | legacy VMSS deployment path | none yet | docs and scripts | no | confirm retired |
| root deployment docs referencing workspaces | MERGE | docs need env-root updates | `repos/spendpilot-docs/` updated runbooks | root README and deployment docs | no | doc update review |

## Notes

- No infra/deployment files were deleted in this pass.
- Unsafe items remain intentionally classified as `REVIEW`.
