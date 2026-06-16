# Migration Checklist

Last updated: 2026-06-16

## Product Validation Carry-Forward

- [x] Record the remaining PostgreSQL validation gap
- [x] Record user approval to proceed with planning despite that gap
- [ ] Validate PostgreSQL migrations in a real PostgreSQL runtime

## Repo Split Preparation

- [x] Identify current monorepo layout
- [x] Define target repo layout
- [x] Define service boundaries
- [x] Define split-readiness per service area
- [x] Define local-dev expectations after split
- [x] Classify code and docs cleanup candidates
- [ ] Physically move frontend into future `repos/spendpilot-frontend`
- [ ] Physically move backend into future `repos/spendpilot-services`
- [ ] Physically move docs into future `repos/spendpilot-docs`
- [ ] Validate imports, local commands, Dockerfiles, and tests after moves
- [ ] Delete old app locations after successful validation

## Infra And Deployment Preparation

- [x] Document current Terraform, Helm, raw-manifest, and workflow layout
- [x] Define target infra repo/module/environment layout
- [x] Define state migration approach
- [x] Define shared-resource ownership model
- [x] Define Front Door origin contract
- [x] Define security baseline
- [x] Define Helm target structure
- [x] Define GitOps target structure
- [x] Define CI/CD target structure
- [x] Classify infra/deployment cleanup candidates
- [ ] Create target env-root Terraform structure
- [ ] Migrate shared ACR into `global-shared`
- [ ] Migrate non-prod Front Door into `nonprod-shared`
- [ ] Migrate prod Front Door into `prod`
- [ ] Bootstrap kGateway and ArgoCD via Terraform modules
- [ ] Create GitOps environment applications
- [ ] Replace legacy Terraform workspace flow
- [ ] Replace old workflow files and deployment scripts after validation

## Validation

- [x] Document validation commands and blockers
- [ ] Run Terraform fmt/validate/plan for all target roots
- [ ] Run Helm lint and templates for all target env values
- [ ] Validate GitOps YAML
- [ ] Validate GitHub Actions workflow syntax in the new structure
- [ ] Build affected Docker images in the final structure
- [ ] Run repository-wide scans for removed or replaced paths

## Cleanup

- [x] Build cleanup plans before deletion
- [ ] Remove only files classified as safe `DELETE`
- [ ] Re-run validation after cleanup
- [ ] Publish final post-execution cleanup report
