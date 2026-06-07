# Authentication context

Production auth model:

- Microsoft Entra ID
- multitenant app registrations with `common` authority
- frontend SPA obtains API tokens with MSAL
- backend validates Entra JWTs and enforces tenant-aware RBAC
- user sessions are stored in the application database
- frontend API scopes must use the backend Application ID URI, not the backend client ID
- backend token validation accepts the configured Application ID URI and both client-ID audience forms to tolerate Microsoft v2 token audience differences across personal and organizational accounts

Role model:

- `platform_admin`
- `org_admin`
- `finance_manager`
- `approver`
- `auditor`
- `employee`

Bootstrap behavior:

- one organization is created per Entra tenant ID for workforce accounts
- one isolated workspace is created per personal Microsoft account
- the first user from a tenant becomes `org_admin`
- platform admins can also be injected with `PLATFORM_ADMIN_EMAILS`
- end users do not need pre-registration in the app; first successful sign-in bootstraps the account automatically

Dev fallback:

- `AUTH_MODE=dev-local`
- `NEXT_PUBLIC_AUTH_MODE=dev-local`
- `POST /api/auth/dev-login`
