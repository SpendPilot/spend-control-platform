# Security Baseline

Last updated: 2026-06-16

## Dev

- public AKS acceptable
- least-privilege managed identities where practical
- no long-lived Azure secrets in Kubernetes when workload identity is available
- keep non-prod approvals lighter but still gated for infra apply

## Staging

- mirror prod auth and identity posture as closely as possible
- keep workload identity enabled
- restrict write access to deployment workflows

## Prod

- public AKS for now, but with explicit hardening
- prefer authorized IP ranges if operationally feasible
- enable Azure RBAC where supported
- disable local admin accounts if feasible without breaking operations
- use managed identity and workload identity
- move toward private endpoints/private DNS where worth the complexity

## Public Prod AKS Controls

- API server remains public for current target state
- document future migration to private AKS
- avoid admin kubeconfigs in normal automation flows

## Secret Handling

- prefer Key Vault and workload identity
- do not store long-lived Azure client secrets in GitHub if OIDC can be used
- never commit real secrets, tfstate, kubeconfigs, or certificates

## CI/CD

- GitHub environment approvals for staging/prod
- OIDC to Azure where possible
- immutable image tags
- no `latest` tag in prod promotion flow

## Future Hardening TODOs

- evaluate private AKS
- evaluate private endpoints for storage, database, and key services
- formalize production break-glass procedure
