# Deployment context

Canonical production path:

- `terraform/azure/aks/` provisions Azure and runs Helm
- `infra/helm/business-ai-app/` defines the in-cluster application topology
- `infra/k8s/` mirrors the same shape as raw YAML

Key deployment choices:

- no Kubernetes Ingress
- Gateway API and kGateway only
- Front Door Premium with WAF as the public edge
- Front Door forwards to the gateway over HTTPS, not HTTP
- backend is split into `identity`, `finance`, and `documents` services on AKS
- local docker compose stays combined for simplicity
- kGateway charts are vendored from the official `kgateway-dev/kgateway` `v2.3.0` source tree under `infra/vendor/kgateway/`
- the app namespace is created by Terraform with `kubernetes_namespace`; the Helm release does not create it
- the Helm migration job must stay `post-install,post-upgrade`

Live-tested Azure findings from June 8, 2026:

- `Central India` in the tested subscription had no usable `Standard_DSv5` quota, so AKS uses `Standard_D2s_v3`
- PostgreSQL HA plus geo-backup required a move from the original Burstable SKU to `GP_Standard_D2s_v3`
- the tested Azure AI Foundry deployment path for `gpt-4.1-mini` worked in `East US 2`, not in the attempted Central India configuration
- local `az acr build` can fail behind SSL interception; GitHub-backed ACR Tasks are the reliable fallback
- Front Door can return a temporary platform `404` while edge configuration propagates even after the Azure resource `provisioningState` is `Succeeded`
- the frontend must not rely on build-time `NEXT_PUBLIC_*` injection for Entra config; runtime config is served from `/runtime-config`
- Terraform now uses frontend and backend source-tree hashes both to trigger image rebuilds and to force Helm rollouts when source changes
- the gateway TLS secret is created during Terraform apply through Azure CLI plus `kubectl apply`
- the storage account defaults to OAuth auth and disables local users, but shared-key auth stays enabled because the current AzureRM provider still expects it for storage-account management
