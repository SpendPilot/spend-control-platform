# Azure Entra Setup

Terraform now creates the core app registrations:

1. frontend SPA app registration
2. backend API app registration

Backend API registration:

- supported account types: `AzureADandPersonalMicrosoftAccount`
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

- supported account types: `AzureADandPersonalMicrosoftAccount`
- authority: `https://login.microsoftonline.com/common`
- requested access token version: `2`
- local redirect URI for `http://localhost:3000/login`
- Front Door login redirect URI based on the deployed endpoint hostname

Customer tenant onboarding still requires tenant admin consent and role assignment in the customer tenant because this is a multi-tenant SaaS model.

Personal Microsoft accounts are only supported for platform-owner access. The backend accepts personal accounts only when the email is listed in `PLATFORM_ADMIN_EMAILS`. Customer company users must still use work or school accounts from their own Entra tenants.
