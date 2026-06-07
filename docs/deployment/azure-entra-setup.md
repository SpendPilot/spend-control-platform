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
- request the API scope as `<backend Application ID URI>/access_as_user`
- local redirect URI for `http://localhost:3000/login`
- Front Door login redirect URI based on the deployed endpoint hostname

Customer tenant onboarding still requires tenant admin consent and role assignment in the customer tenant because this is a multi-tenant SaaS model.

Personal Microsoft accounts are also supported. The application creates one isolated workspace per personal Microsoft account so consumer users do not collapse into the shared Microsoft consumer tenant.
