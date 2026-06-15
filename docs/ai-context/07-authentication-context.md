# Authentication context

Production auth model:

- Microsoft Entra ID
- multitenant app registrations with `common` authority
- frontend SPA obtains API tokens with MSAL
- backend validates Entra JWTs and enforces tenant-aware RBAC
- user sessions are stored in the application database
- frontend API scopes must use the backend Application ID URI, not the backend client ID
- backend token validation accepts the configured Application ID URI and both client-ID audience forms to tolerate Microsoft v2 token audience differences across personal and organizational accounts
- Entra app registrations bundle consent between the frontend SPA and backend API via known client applications and pre-authorization for the `access_as_user` scope

Role model:

- `platform_admin`
- `org_admin`
- `finance_manager`
- `approver`
- `auditor`
- `employee`

Bootstrap behavior:

- one organization is created per Entra tenant ID for workforce accounts
- one isolated workspace is created per true Microsoft consumer-tenant account
- guest Microsoft accounts invited into a workforce tenant stay inside that tenant workspace
- the first user from a tenant becomes `org_admin`
- platform admins can also be injected with `PLATFORM_ADMIN_EMAILS`
- end users do not need pre-registration in the app; first successful sign-in bootstraps the account automatically
- external customer-tenant service principals are created by consent in that tenant, not directly by Terraform in the home tenant

Dev fallback:

- `AUTH_MODE=dev-local`
- `NEXT_PUBLIC_AUTH_MODE=dev-local`
- `POST /api/auth/dev-login`
