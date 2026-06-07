# Azure Infrastructure

Canonical Azure target:

```txt
Azure Front Door Premium + WAF
  -> kGateway public service on AKS
  -> HTTPRoutes
      -> frontend
      -> identity-service
      -> finance-service
      -> documents-service

AKS
  -> user-assigned managed identity via Workload Identity
  -> PostgreSQL Flexible Server
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
- `Standard_D2s_v5` node sizing by default
- Central India default region
- one managed identity shared by the application pods
- Entra multi-tenant app registrations created during Terraform apply
- Terraform uses Azure CLI during apply for `az acr build` and `az aks command invoke`
