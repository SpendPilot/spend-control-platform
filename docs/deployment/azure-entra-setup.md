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

Customer tenant onboarding does not require the user to be pre-created inside the app database.

- The first successful browser sign-in bootstraps the user automatically.
- If the customer's Entra tenant allows user consent, a normal user can complete the first sign-in flow.
- If the customer's Entra tenant blocks user consent, a tenant admin must grant consent to the Enterprise Application first.
- Tenant-side app role assignment is optional in this repo because the app can also manage tenant roles internally after bootstrap.

Personal Microsoft accounts are also supported. The application creates one isolated workspace per personal Microsoft account so consumer users do not collapse into the shared Microsoft consumer tenant.
