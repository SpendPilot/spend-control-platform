# Infra Refactor Plan

Last updated: 2026-06-16

## Current Infra Layout

- `terraform/azure/aks/`
  - current AKS-focused Azure bootstrap
  - includes workspace-oriented helper and direct workflow integration
- `terraform/azure/vm-docker/`
  - legacy VM/docker path with local state files present
- `infra/helm/business-ai-app/`
  - current canonical application chart
- `infra/k8s/`
  - raw manifests overlapping with Helm deployment shape
- `.github/workflows/terraform-dev.yml`
  - direct workspace-based plan/apply workflow

## Target Infra Layout

```txt
repos/spendpilot-infra/
  modules/
    resource-group/
    networking/
    aks/
    acr/
    postgres/
    storage/
    keyvault/
    ai-services/
    monitoring/
    managed-identity/
    workload-identity/
    frontdoor/
    private-endpoint/
    private-dns/
    kgateway-bootstrap/
    argocd-bootstrap/
  envs/
    global-shared/
    nonprod-shared/
    dev/
    staging/
    prod/
```

## Module Strategy

- Extract reusable Azure building blocks into `modules/`
- Keep environment composition in `envs/*`
- Bootstrap only platform components from Terraform
- Keep application service rollout in Helm/GitOps

## Environment Strategy

- `global-shared`: ACR and truly global identities
- `nonprod-shared`: Front Door and optional shared non-prod AI services
- `dev`, `staging`, `prod`: full runtime ownership, with prod also owning prod edge

## State Strategy

- Azure Blob backend
- one root module per environment/shared scope
- no workspaces for environment separation
- state keys:
  - `global-shared.tfstate`
  - `nonprod-shared.tfstate`
  - `dev.tfstate`
  - `staging.tfstate`
  - `prod.tfstate`

## Workspace Removal Plan

- retire `terraform workspace select dev` flow
- replace `dev-workspace.ps1` with env-specific backend/init conventions
- remove workflow dependence on workspace-only state once new roots validate

## Shared Resource Strategy

- ACR in `global-shared`
- non-prod Front Door in `nonprod-shared`
- prod Front Door in `prod`
- shared-origin dependencies flow from env outputs to shared state reads

## Apply Order

1. `global-shared`
2. `nonprod-shared` initial
3. `dev`
4. `staging`
5. `nonprod-shared` second pass for origins/routes
6. `prod`

## Validation Commands

- `terraform fmt -recursive`
- `terraform validate` for each env
- `terraform plan` for each env
- `helm lint`
- `helm template` per env
- GitOps YAML validation
- workflow syntax validation

## Risks

- legacy workspace state and new env-root state can conflict if migration is not sequenced carefully
- legacy VM/docker Terraform may still own resources historically
- raw manifests and Helm can create duplicate active deployment paths

## Rollback Notes

- back up state before any migration
- do not delete old roots until new roots are validated
- if plan shows duplicate ownership, stop and resolve before apply
