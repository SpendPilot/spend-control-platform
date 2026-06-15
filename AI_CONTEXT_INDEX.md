# AI Context Index

Last updated: 2026-06-15

## Read First

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `IMPLEMENTATION_CHECKLIST.md`
4. `RISK_REGISTER.md`
5. `DECISIONS.md`
6. `FINAL_AI_CONTEXT_HANDOFF.md`
7. `docs/ai-context/`

## Source Of Truth Hierarchy

- Product mission and safety rules: `AGENTS.md`
- Current implementation state: `CURRENT_STATE.md`
- Decisions: `DECISIONS.md`
- Risks and blockers: `RISK_REGISTER.md`
- Final current-run handoff: `FINAL_AI_CONTEXT_HANDOFF.md`
- Detailed runtime/architecture history: `docs/ai-context/`

## Repository Status

- This is still the original unsplit `SpendPilot` repository.
- Repo split, CI/CD restructure, and Terraform/Helm/GitOps restructuring were not executed in this run.
- Product refactor work was kept compatible with later repo/platform refactor prompts.

## Core Context Files

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Active product-refactor mission and safety rules |
| `CURRENT_STATE.md` | Current product-refactor state and phase status |
| `IMPLEMENTATION_CHECKLIST.md` | Phase completion and remaining gaps |
| `DECISIONS.md` | ADR-style decisions for the current refactor |
| `RISK_REGISTER.md` | Active risks and review-required areas |
| `PRODUCT_REFOCUS_PLAN.md` | Mapping from original product shape to payment-ops target |
| `CURRENT_FEATURE_MAP.md` | Current feature inventory |
| `DATA_MODEL_CHANGELOG.md` | Additive schema-change notes |
| `CLEANUP_REFOCUS_PLAN.md` | Conservative cleanup planning |
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
- If context conflicts are found, record them in `DECISIONS.md` or `RISK_REGISTER.md` before choosing a direction.
- Do not treat repo-split or infra-refactor plan files as active scope while product refactor validation remains incomplete.
