# Cleanup Refocus Plan

Last updated: 2026-06-16

## KEEP

- existing auth and tenant bootstrap code
- existing document extraction pipeline
- existing infra / terraform / helm / deployment assets

## MERGE

- older generic expense UX into the new payment-ops surfaces over time
- older settings/admin surface into the org-owner departments-and-users workspace

## REVIEW

- `docs/deployment/azure-entra-setup.md`
- older frontend wording that still references the pre-payment-ops workspace
- whether `/approvals` remains necessary after UX consolidation

## DELETE

- None in this run

## Notes

- 2026-06-16: Cleanup review was repeated after backend, frontend, and SQLite migration validation.
- 2026-06-16: No safe product-level deletions were identified that would improve the repo without adding risk ahead of the later repo/platform refactor prompts.
