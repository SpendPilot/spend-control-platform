# Frontend context

Runtime auth configuration must come from the deployed container environment, not from Next.js build-time inlined `NEXT_PUBLIC_*` values.

Current pattern:

- the frontend loads `/runtime-config` before interactive hydration
- `/runtime-config` is a Next.js route handler that reads runtime env vars from the container
- `window.__APP_CONFIG__` is the primary client-side config source for Entra and API routing

The frontend lives in `frontend/` and is the finance workspace for the platform.

Pages now kept:

- `/`
- `/login`
- `/dashboard`
- `/expenses`
- `/approvals`
- `/spend-limits`
- `/payment-priority`
- `/ai-insights`
- `/budgets`
- `/documents`
- `/documents/[id]`
- `/profile`
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

2026-06-15 Phase 1 note:

- added `/onboarding` for employee department selection
- `frontend/components/app-shell.tsx` now redirects employee users without completed onboarding to `/onboarding`
- full role-specific layouts are intentionally deferred to later product-refactor phases

2026-06-15 continued refactor note:

- `frontend/components/app-shell.tsx` now exposes role-aware navigation for org owners, dept heads, and employees
- the frontend currently implements the requested product pages as a functional baseline on top of the existing app routes
