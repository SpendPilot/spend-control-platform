# Cleanup Plan

Last updated: 2026-06-16

| Path | Classification | Reason | Replacement path | References found | Safe to remove now | Validation required before removal |
| --- | --- | --- | --- | --- | --- | --- |
| `frontend/` | MOVE | future standalone app repo | `repos/spendpilot-frontend/` | root README, compose, docs, frontend docs | no | frontend build/tests and path updates |
| `backend/` | MOVE | future standalone services repo | `repos/spendpilot-services/` | root README, compose, docs, Docker references | no | backend tests, image builds, import/path updates |
| `docs/` | MOVE | future standalone docs repo | `repos/spendpilot-docs/` | root README and deployment docs | no | doc link updates |
| `infra/helm/business-ai-app/` | MOVE | future standalone Helm repo | `repos/spendpilot-helm/charts/spendpilot/` | README, workflow, docs, terraform references | no | helm lint/template in new location |
| `infra/k8s/` | REVIEW | overlaps with Helm and may be obsolete or fallback-only | likely Helm/GitOps-managed replacements | root README, deployment docs | no | confirm no operational dependency remains |
| `infra/vm/` | REVIEW | historical VM deployment path | none yet | docs and local scripts | no | confirm no live dependency |
| `infra/vmss/` | REVIEW | historical VMSS deployment path | none yet | docs and local scripts | no | confirm no live dependency |
| `terraform/azure/aks/` | MOVE | future env-root infra repo source | `repos/spendpilot-infra/envs/*` plus `modules/` | root README, workflow, deployment docs | no | terraform validate/plan after restructure |
| `terraform/azure/aks/dev-workspace.ps1` | DELETE | workspace-based helper conflicts with target env-root strategy | env folders and explicit backend configs | root README and workflow path references | no | replacement infra workflow validated |
| `terraform/azure/vm-docker/` | REVIEW | legacy infra path with local tfstate files | likely retired after AKS migration | docs and local infra history | no | confirm no state/resource ownership remains |
| `.github/workflows/terraform-dev.yml` | REVIEW | applies workspace-based Terraform directly against current AKS path | future env-aware infra workflows | workflow refs in README/docs | no | new CI/CD structure validated |
| `docker-compose.yml` | KEEP | current local dev entrypoint | future services/frontend local-dev equivalents | README, docs | yes | n/a |
| root deployment READMEs | MERGE | some overlap with docs repo target | `repos/spendpilot-docs/` | root references | no | doc consolidation review |

## Notes

- `terraform.tfstate` and `terraform.tfstate.backup` under `terraform/azure/vm-docker/` are never auto-delete targets.
- No file above is authorized for deletion in this pass.
