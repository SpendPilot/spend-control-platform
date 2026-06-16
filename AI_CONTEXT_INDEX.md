# AI Context Index

Last updated: 2026-06-16

## Read First

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `IMPLEMENTATION_CHECKLIST.md`
4. `RISK_REGISTER.md`
5. `DECISIONS.md`
6. `FINAL_AI_CONTEXT_HANDOFF.md`
7. `AI_CONTEXT.md`
8. `TARGET_ARCHITECTURE.md`
9. `REFACTOR_PLAN.md`
10. `docs/ai-context/`

## Source Of Truth Hierarchy

- Product mission and safety rules: `AGENTS.md`
- Current implementation state: `CURRENT_STATE.md`
- Repo/platform planning entrypoint: `AI_CONTEXT.md`
- Target repo/platform architecture: `TARGET_ARCHITECTURE.md`
- Repo/platform phase plan: `REFACTOR_PLAN.md`
- Decisions: `DECISIONS.md`
- Risks and blockers: `RISK_REGISTER.md`
- Final current-run handoff: `FINAL_AI_CONTEXT_HANDOFF.md`
- Detailed runtime/architecture history: `docs/ai-context/`

## Repository Status

- This is still the original unsplit `SpendPilot` repository.
- Repo split, CI/CD restructure, and Terraform/Helm/GitOps restructuring were not executed in this run.
- Product refactor work was kept compatible with later repo/platform refactor prompts.
- 2026-06-16: repo/platform planning and handoff docs were completed, but physical split and infra migration were not executed.

## Core Context Files

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Active product-refactor mission and safety rules |
| `AI_CONTEXT.md` | Repo/platform planning entrypoint and constraints |
| `CURRENT_STATE.md` | Current product-refactor state and phase status |
| `TARGET_ARCHITECTURE.md` | Target repo/platform/application architecture |
| `REFACTOR_PLAN.md` | High-level repo/platform phase plan |
| `IMPLEMENTATION_CHECKLIST.md` | Phase completion and remaining gaps |
| `MIGRATION_CHECKLIST.md` | Repo/platform/infrastructure migration checklist |
| `DECISIONS.md` | ADR-style decisions for the current refactor |
| `RISK_REGISTER.md` | Active risks and review-required areas |
| `CLEANUP_STRATEGY.md` | Cleanup rules for repo/platform work |
| `PRODUCT_REFOCUS_PLAN.md` | Mapping from original product shape to payment-ops target |
| `CURRENT_FEATURE_MAP.md` | Current feature inventory |
| `DATA_MODEL_CHANGELOG.md` | Additive schema-change notes |
| `CLEANUP_REFOCUS_PLAN.md` | Conservative cleanup planning |
| `SERVICE_BOUNDARIES.md` | Service decomposition plan for future split |
| `SERVICE_SPLIT_READINESS.md` | Split-readiness assessment by service area |
| `LOCAL_DEV.md` | Current and future local-development guidance |
| `REPO_SPLIT_PLAN.md` | Monorepo-to-multi-repo migration plan |
| `CLEANUP_PLAN.md` | App/repo cleanup classification table |
| `CLEANUP_REPORT.md` | Current cleanup execution status for repo/platform planning |
| `INFRA_REFACTOR_PLAN.md` | Target infra repo/module/environment plan |
| `STATE_MIGRATION_PLAN.md` | Terraform state migration strategy |
| `SHARED_RESOURCE_STRATEGY.md` | Shared Azure resource ownership plan |
| `FRONTDOOR_ORIGIN_STRATEGY.md` | Shared Front Door ownership and output contract |
| `SECURITY_BASELINE.md` | Target environment security baseline |
| `HELM_REFACTOR_PLAN.md` | Helm repo/chart refactor plan |
| `GITOPS_STRATEGY.md` | ArgoCD/GitOps target design |
| `CICD_STRATEGY.md` | CI/CD target design |
| `CLEANUP_INFRA_DEPLOYMENT_PLAN.md` | Infra/deployment cleanup classification table |
| `FINAL_REFACTOR_SUMMARY.md` | Final repo/platform planning summary |
| `FINAL_FOLDER_STRUCTURE.md` | Current and future folder-structure summary |
| `FINAL_PRODUCT_SUMMARY.md` | Final current-run product summary |
| `FINAL_FEATURE_MAP.md` | Final current-run feature map |
| `FINAL_ROLE_ACCESS_MATRIX.md` | Final role matrix |
| `FINAL_API_MAP.md` | Final API inventory |
| `FINAL_DATA_MODEL.md` | Final data model snapshot |
| `FINAL_OPERATIONS_GUIDE.md` | Current operations and validation guide |
| `FINAL_CLEANUP_REPORT.md` | Cleanup decisions and execution status |
| `FINAL_AI_CONTEXT_HANDOFF.md` | Handoff for future agents |
| `docs/ai-context/` | Detailed runtime, architecture, auth, database, deployment, and refactor history |

## Required Agent Notes

- Future agents should read `AGENTS.md`, `CURRENT_STATE.md`, and `FINAL_AI_CONTEXT_HANDOFF.md` before changing application code.
- Future agents doing repo/platform work should also read `AI_CONTEXT.md`, `TARGET_ARCHITECTURE.md`, `REFACTOR_PLAN.md`, and `MIGRATION_CHECKLIST.md`.
- If context conflicts are found, record them in `DECISIONS.md` or `RISK_REGISTER.md` before choosing a direction.
- Do not treat repo-split or infra-refactor planning docs as proof that the physical migration already happened.
