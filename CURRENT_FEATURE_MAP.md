# Current Feature Map

Last updated: 2026-06-15

## Implemented

### Identity and tenancy

- Entra-backed auth plus `dev-local`
- automatic org bootstrap per tenant/workspace
- first membership in a tenant becomes `org_owner`
- department onboarding for employees
- dept-head promotion and demotion controls
- tenant-scoped session tracking

### Finance

- expense categories
- budget CRUD with company/department scope fields
- variable expense submission and approval lifecycle
- recurring expenses
- recurring expense requests
- spend limits
- payment-priority and cash-outflow baseline
- dashboard summary with budget, category, department, and payment-priority data

### Documents and AI

- file upload
- blob/local storage abstraction
- OCR and invoice extraction
- AI analysis and fallback extraction
- document-to-expense linking
- bills-library baseline
- tenant-scoped AI chat sessions and grounded assistant responses

### Admin

- organization membership listing
- membership role/status/department update
- department listing
- session listing and revocation
- audit-event listing

### Frontend

- role-aware navigation baseline
- onboarding page
- org-owner workspace pages
- dept-head workspace pages
- employee workspace pages

## Still Incomplete Or Needing Refinement

- frontend build/lint/type validation
- PostgreSQL migration validation
- UX polish for some owner/dept-head flows
- conservative cleanup execution
