# Spend Control Helm Chart

This chart deploys:

- `spend-control-frontend`
- `spend-control-identity`
- `spend-control-finance`
- `spend-control-documents`
- migration job
- service account with optional workload identity annotation
- Gateway API `Gateway`
- HTTPRoutes for frontend, identity, finance, and documents paths

## Render

```bash
helm template spend-control infra/helm/business-ai-app
```

## Install

```bash
helm upgrade --install spend-control infra/helm/business-ai-app \
  --namespace spend-control \
  --create-namespace \
  -f infra/helm/business-ai-app/values-prod.yaml
```

Important values:

- image repositories and tag
- `auth.frontendClientId`
- `auth.backendClientId`
- `auth.backendAudience`
- `auth.apiScope`
- `azure.managedIdentityClientId`
- `azure.aiFoundryEndpoint`
- `azure.documentIntelligenceEndpoint`
- `azure.storageAccountUrl`
- `secrets.databaseUrl`

Auth note:

- `auth.apiScope` should be `<backend Application ID URI>/access_as_user`
- do not derive it from the backend client ID unless your Application ID URI actually uses `api://<clientId>`
