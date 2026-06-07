# Refactor log

Latest major refactor:

1. validated the repo and docs against the current runtime
2. expanded the backend from a small document scanner into a tenant-aware finance platform
3. introduced organizations, memberships, sessions, budgets, expenses, approvals, and audit events
4. split the AKS backend runtime into identity, finance, and documents services
5. upgraded document processing to include invoice extraction
6. rewired Helm and raw manifests to use Gateway API HTTPRoutes
7. replaced the AKS Terraform path with Front Door + WAF + kGateway + Workload Identity bootstrap
8. updated README, deployment docs, and AI context files
9. corrected Entra API scope wiring to use the backend Application ID URI
10. refactored auth bootstrap so personal Microsoft accounts get isolated workspaces instead of being rejected or merged together
11. hardened frontend API URL building so `/api` base paths cannot turn into `/api/api/...` during login callbacks

Intentional simplification kept:

- local docker compose still uses the combined backend entrypoint for easier development
