# Azure Infrastructure

Canonical Azure target:

```txt
Azure Front Door Premium + WAF
  -> HTTPS to the kGateway public service on AKS
  -> HTTPRoutes
      -> frontend
      -> identity-service
      -> finance-service
      -> documents-service

AKS
  -> user-assigned managed identity via Workload Identity
  -> PostgreSQL Flexible Server (General Purpose, zone-redundant HA, geo-backup)
  -> Blob Storage
  -> Azure AI Foundry account + model deployment
  -> Azure AI Document Intelligence account
```

Provisioning source of truth:

- `terraform/azure/aks/`

Application deployment source of truth:

- `infra/helm/business-ai-app/`

Key design points:

- minimal AKS node pools: one system pool and one user pool
- `Standard_D2s_v3` node sizing in the validated subscription because `Standard_DSv5` quota was unavailable in `Central India`
- PostgreSQL uses `GP_Standard_D2s_v3` because the original Burstable SKU could not satisfy the approved HA + geo-backup target
- Central India remains the default region for the core platform
- Azure AI Foundry is intentionally separated to `East US 2` in the validated path
- one managed identity shared by the application pods
- Entra multi-tenant app registrations created during Terraform apply
- Terraform uses Azure CLI during apply for `az acr build` and `az aks command invoke`
- the validated fallback for restricted laptops is GitHub-backed ACR Tasks plus `build_images_during_apply=false`
- kGateway is installed from the vendored official chart source in `infra/vendor/kgateway/`
- Front Door probes the AKS origin over `HTTPS` on `/health`
- the WAF policy includes an auth rate-limit rule for `/api/auth`
- the storage account defaults to OAuth auth and keeps local users disabled; shared-key auth stays enabled only to preserve Terraform/AzureRM management compatibility
