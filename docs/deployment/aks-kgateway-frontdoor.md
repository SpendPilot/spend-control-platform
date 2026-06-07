# AKS, Front Door, WAF, and kGateway

This repository now targets:

```txt
User
  -> Azure Front Door Premium
  -> WAF policy
  -> kGateway service on AKS
  -> Gateway API HTTPRoutes
  -> frontend / identity / finance / documents services
```

Routing rules:

- `/` -> `spend-control-frontend`
- `/api/auth`, `/api/admin`, `/health`, `/ready` -> `spend-control-identity`
- `/api/finance` -> `spend-control-finance`
- `/api/documents`, `/api/ai` -> `spend-control-documents`

Operational notes:

- Front Door probes `/health`
- kGateway is the only public AKS entrypoint
- Backend services stay `ClusterIP`
- Browser traffic should keep `NEXT_PUBLIC_API_BASE_URL=/api`
- Front Door default domain is used by default; custom domains can be added later
- The kGateway chart is vendored in `infra/vendor/kgateway/` to avoid OCI pull issues in restricted networks
- The app namespace is created by Terraform before the Helm release; the chart itself should not also be relied on for namespace bootstrap
- The migration job is a post-install and post-upgrade hook because it depends on the chart-created ServiceAccount and Secret
- The AKS gateway service is a `LoadBalancer` service named `spend-control-gateway`
- Front Door may take additional time to propagate even after `provisioningState` is `Succeeded`
- The validated route forwards HTTP from Front Door to the AKS gateway while Front Door still redirects clients to HTTPS at the edge
