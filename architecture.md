# Architecture Summary

```txt
Azure Front Door Premium + WAF
  -> kGateway on AKS
    -> HTTPRoute /
      -> spend-control-frontend
    -> HTTPRoute /api/auth, /api/admin, /health, /ready
      -> spend-control-identity
    -> HTTPRoute /api/finance
      -> spend-control-finance
    -> HTTPRoute /api/documents, /api/ai
      -> spend-control-documents
```

Shared platform services:

- PostgreSQL Flexible Server for tenant, finance, and document metadata
- Azure Blob Storage for uploaded files
- Azure AI Document Intelligence for OCR and invoice extraction
- Azure AI Foundry for finance-aware document analysis
- Azure Workload Identity with one user-assigned managed identity for AKS workloads

Identity and tenancy model:

- Multi-tenant SaaS
- One organization per Entra tenant by default
- First user in a tenant is bootstrapped as `org_admin`
- Roles: `platform_admin`, `org_admin`, `finance_manager`, `approver`, `auditor`, `employee`
- Session records are stored in the application database and can be revoked at the org admin layer
