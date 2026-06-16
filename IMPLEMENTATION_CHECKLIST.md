# Implementation Checklist

Last updated: 2026-06-16

## Phase -1

- [x] Read `AGENTS.md`
- [x] Scan repository for AI/context files and agent instructions
- [x] Read discovered context files
- [x] Create repo-level context tracking docs
- [x] Confirm unsplit repo and future refactor compatibility constraints

## Phase 0

- [x] Read source-of-truth context docs
- [x] Scan frontend, backend, database, tests, and deployment-relevant project structure
- [x] Identify auth and tenant bootstrap logic
- [x] Identify first-user top-role logic
- [x] Identify bill upload and extraction flow
- [x] Identify current expense, budget, and approval flow
- [x] Create `PRODUCT_REFOCUS_PLAN.md`
- [x] Create `CURRENT_FEATURE_MAP.md`

## Phase 1

- [x] Preserve current authentication behavior
- [x] Preserve first-user org-owner bootstrap behavior
- [x] Add canonical roles: `org_owner`, `dept_head`, `employee`
- [x] Default later users to `employee`
- [x] Add first-login department selection
- [x] Add department assignment model
- [x] Ensure default departments: `IT`, `Marketing`, `HR`
- [x] Add org-owner promote/demote dept-head controls
- [x] Add role and tenant scoped access checks
- [x] Add or update tests
- [x] Update context docs after implementation and validation

## Phase 2

- [x] Extend data model additively for vendors, recurring expenses, recurring requests, spend limits, payment priorities, AI chat, and richer budgets/expenses/documents
- [x] Create additive migration docs and migration files
- [x] Make altered-table migrations validate on SQLite using Alembic batch operations

## Phase 3

- [x] Implement expanded finance APIs
- [x] Implement recurring request / approval APIs
- [x] Implement spend-limit APIs
- [x] Implement payment-priority APIs
- [x] Implement AI chat APIs
- [x] Keep audit logging active

## Phase 4

- [x] Add role-aware navigation baseline
- [x] Preserve onboarding redirect behavior
- [x] Keep pages tenant-scoped
- [x] Role-specific workspace shell and access flow

## Phase 5

- [x] Org-owner dashboard baseline
- [x] Org-owner expenses baseline
- [x] Org-owner spend-limits page baseline
- [x] Org-owner payment-priority page baseline
- [x] Org-owner AI insights page baseline
- [x] Org-owner budgets page baseline
- [x] Org-owner bills-library page baseline
- [x] Org-owner departments/users page baseline
- [x] Org-owner profile page baseline

## Phase 6

- [x] Dept-head dashboard baseline
- [x] Recurring expense request flow
- [x] Employee variable expense review / forward / reject flow
- [x] Department profile baseline

## Phase 7

- [x] Employee department budget view baseline
- [x] Employee variable expense submission flow
- [x] Employee profile baseline

## Phase 8

- [x] Preserve document extraction
- [x] Link extracted documents into variable-expense flow
- [x] Expose bills-library metadata for linked expense context
- [x] Allow frontend expense forms to upload and link supporting bills

## Phase 9

- [x] Weekly cash-outflow calculation baseline
- [x] Monthly cash-outflow calculation baseline
- [x] Payment-priority ranking baseline

## Phase 10

- [x] Tenant-grounded AI assistant baseline
- [x] AI chat history persistence

## Phase 11

- [x] Cleanup planning docs
- [x] Re-run cleanup review after broader validation
- [x] Confirm no safe product-level deletions should be executed in this run

## Phase 12

- [x] Backend tests
- [x] Document validation limits and remaining gaps
- [x] SQLite Alembic upgrade validation
- [x] Frontend build/lint/typecheck
- [ ] PostgreSQL migration validation

## Phase 13

- [x] Final summary docs
- [x] Final API/data/role docs
- [x] Final AI context handoff

## Repo And Platform Planning Follow-Up

- [x] Create `AI_CONTEXT.md`
- [x] Create `TARGET_ARCHITECTURE.md`
- [x] Create `REFACTOR_PLAN.md`
- [x] Create `MIGRATION_CHECKLIST.md`
- [x] Create `CLEANUP_STRATEGY.md`
- [x] Create `SERVICE_BOUNDARIES.md`
- [x] Create `SERVICE_SPLIT_READINESS.md`
- [x] Create `LOCAL_DEV.md`
- [x] Create `REPO_SPLIT_PLAN.md`
- [x] Create `CLEANUP_PLAN.md`
- [x] Create `CLEANUP_REPORT.md`
- [x] Create `INFRA_REFACTOR_PLAN.md`
- [x] Create `STATE_MIGRATION_PLAN.md`
- [x] Create `SHARED_RESOURCE_STRATEGY.md`
- [x] Create `FRONTDOOR_ORIGIN_STRATEGY.md`
- [x] Create `SECURITY_BASELINE.md`
- [x] Create `HELM_REFACTOR_PLAN.md`
- [x] Create `GITOPS_STRATEGY.md`
- [x] Create `CICD_STRATEGY.md`
- [x] Create `CLEANUP_INFRA_DEPLOYMENT_PLAN.md`
- [x] Create `FINAL_REFACTOR_SUMMARY.md`
- [x] Create `FINAL_FOLDER_STRUCTURE.md`
- [ ] Execute physical repo split
- [ ] Execute Terraform/Helm/GitOps/CI-CD migration
- [ ] Run toolchain-dependent validation in a fully equipped environment
