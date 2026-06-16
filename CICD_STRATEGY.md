# CI/CD Strategy

Last updated: 2026-06-16

## Frontend CI

- install
- lint
- typecheck
- build
- Docker build

## Backend/Services CI

- install
- pytest
- service image builds
- optional path-filtered jobs once services are physically separated

## Container Strategy

- push images to shared ACR
- use immutable tags
- do not use `latest` in production

## Helm And GitOps Validation

- lint and template chart changes
- validate GitOps YAML before merge

## Infrastructure Workflow

- plan/apply per environment root, not workspace
- OIDC to Azure where possible
- approvals for staging/prod

## Pull Request Checks

- changed-path filtering
- app tests/builds for app changes
- helm validation for chart changes
- terraform validation for infra changes

## Main Branch Flow

- merge after checks pass
- environment-specific promotion rather than direct prod mutation

## Promotion Flow

- dev -> staging -> prod using the same immutable image tag

## Rollback Flow

- app rollback through GitOps version reversion
- infra rollback through reviewed Terraform change or state-aware corrective work
