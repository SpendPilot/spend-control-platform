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
