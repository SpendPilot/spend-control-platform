# Frontend context

The frontend lives in `frontend/` and is the finance workspace for the platform.

Pages now kept:

- `/`
- `/login`
- `/dashboard`
- `/expenses`
- `/approvals`
- `/budgets`
- `/documents`
- `/documents/[id]`
- `/scan`
- `/settings`

Important frontend files:

- `frontend/components/auth-provider.tsx`
- `frontend/components/app-shell.tsx`
- `frontend/lib/api.ts`
- `frontend/lib/runtime-config.ts`

Frontend assumptions:

- same-origin `/api` is preferred behind Front Door and kGateway
- the browser sees one API base URL, but kGateway splits traffic to identity, finance, and documents services
- `NEXT_PUBLIC_AUTH_MODE=dev-local` is only for local development and tests
