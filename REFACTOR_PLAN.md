# Refactor Plan

Last updated: 2026-06-16

## Status Summary

- Product refactor: functionally complete, with PostgreSQL validation still pending in a proper runtime
- Repo split planning: complete
- Infra/Helm/GitOps/CI-CD planning: complete
- Physical repo split: not executed in this pass
- Infra state migration: not executed in this pass
- Destructive cleanup: not executed in this pass

## Phase Order

1. Stabilize product refactor outputs and record remaining validation gaps.
2. Define future repo split boundaries without breaking the current monorepo.
3. Define target infra, Helm, GitOps, and CI/CD structure.
4. Classify cleanup and migration work before any deletion or state movement.
5. Perform physical split and platform migration only in a validation-capable environment.

## Immediate Deliverables From This Pass

- Repo split documentation
- Service boundary documentation
- Local dev and migration guidance
- Infra/state/Helm/GitOps/CI-CD planning docs
- Cleanup classification docs
- Final summary and folder-structure handoff docs

## Deferred Execution Work

- Move application code into future `repos/` layout
- Replace workspace-based Terraform live flow with env-root state layout
- Create new Helm repo structure and move chart into it
- Create GitOps desired-state repo structure
- Replace direct Terraform apply workflow with environment-aware pipelines
- Delete legacy VM, VMSS, raw-manifest, or old Terraform paths after validation

## Completion Rule

Planning is complete only when all target structures, migration order, risks, and cleanup classifications are documented.
Execution is complete only after physical moves, validations, and safe cleanup are run in an environment with the required toolchain and cloud access.
