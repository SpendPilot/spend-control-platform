# Azure Entra Setup

Terraform now creates the core app registrations:

1. frontend SPA app registration
2. backend API app registration

Backend API registration:

- multi-tenant audience: `AzureADMultipleOrgs`
- application ID URI: `api://<prefix>-<env>-api`
- scope: `access_as_user`
- app roles:
  - `platform_admin`
  - `org_admin`
  - `finance_manager`
  - `approver`
  - `auditor`
  - `employee`

Frontend SPA registration:

- multi-tenant audience: `AzureADMultipleOrgs`
- local redirect URI for `http://localhost:3000/login`
- Front Door login redirect URI based on the deployed endpoint hostname

Customer tenant onboarding still requires tenant admin consent and role assignment in the customer tenant because this is a multi-tenant SaaS model.
