# Authentication context

Production auth model:

- Microsoft Entra ID
- multi-tenant app registrations
- frontend SPA obtains API tokens with MSAL
- backend validates Entra JWTs and enforces tenant-aware RBAC
- user sessions are stored in the application database

Role model:

- `platform_admin`
- `org_admin`
- `finance_manager`
- `approver`
- `auditor`
- `employee`

Bootstrap behavior:

- one organization is created per Entra tenant ID
- the first user from a tenant becomes `org_admin`
- platform admins can also be injected with `PLATFORM_ADMIN_EMAILS`

Dev fallback:

- `AUTH_MODE=dev-local`
- `NEXT_PUBLIC_AUTH_MODE=dev-local`
- `POST /api/auth/dev-login`
