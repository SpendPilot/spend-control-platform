# Target architecture

```txt
User
  -> Azure Front Door Premium + WAF
  -> kGateway service on AKS
  -> HTTPRoutes
      -> frontend
      -> identity-service
      -> finance-service
      -> documents-service
  -> PostgreSQL Flexible Server
  -> Azure Blob Storage
  -> Azure AI Foundry
  -> Azure AI Document Intelligence
```

Target deployment characteristics:

- multi-tenant Entra SaaS
- one system node pool and one user node pool
- `Standard_D2s_v5` nodes by default
- Workload Identity with one user-assigned managed identity
- Helm-managed application deployments
