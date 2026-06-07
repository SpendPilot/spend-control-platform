# Authentication context

Production auth model:

- Microsoft Entra ID
- multitenant app registrations with `common` authority
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
- personal Microsoft accounts are only accepted when their email is in `PLATFORM_ADMIN_EMAILS`
- those personal platform admins are mapped into the internal `Platform Operations` organization instead of a customer tenant

Dev fallback:

- `AUTH_MODE=dev-local`
- `NEXT_PUBLIC_AUTH_MODE=dev-local`
- `POST /api/auth/dev-login`
