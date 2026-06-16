# Service Split Readiness

Last updated: 2026-06-16

| Area | Current Readiness | Blockers | Shared Dependencies | Database Dependency | API Dependency | Required Future Work | Suggested Future Repo | Suggested Future CI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frontend | Medium | still references monorepo-relative docs and root workflows | env templates, shared contracts assumptions | indirect only through backend APIs | identity, finance, documents APIs | isolate repo-specific README, env, Docker, build workflow | `spendpilot-frontend` | lint, typecheck, build, Docker build |
| Identity service | Medium | shared backend packaging and model imports | auth/config/rbac helpers | high | consumed by frontend and other services | extract service package boundary and shared auth lib | `spendpilot-services` initially, later `spendpilot-identity-service` | pytest, image build |
| Finance service | Medium | shared backend packaging and model imports | config, audit, auth | high | consumed by frontend, AI, documents | isolate service entrypoint, trim cross-imports, document contract | `spendpilot-services` initially, later `spendpilot-finance-service` | pytest, image build |
| Documents service | Medium | shared backend packaging and model imports | storage, auth, config | medium | consumed by frontend and finance linking flows | isolate storage/extraction boundary and service packaging | `spendpilot-services` initially, later `spendpilot-documents-service` | pytest, image build |
| AI logic | Low-Medium | tightly coupled to finance context and shared services | config, auth, finance summarization | low-medium | frontend AI pages rely on finance/document context | decide whether to remain part of finance service or become separate internal module | remain inside `spendpilot-services` for now | pytest, mocked AI tests |
| Shared libs | Low | current code not yet physically separated | every shared utility | n/a | n/a | create minimal technical shared libs only after service folders exist | `spendpilot-services/libs` | unit tests |

## Overall Assessment

- The backend is microservice-ready in runtime shape, but not yet physically split.
- The best next step is a `services/` repo grouping, not seven separate repos immediately.
- A single database remains the biggest architectural coupling.
- Code movement should happen after a validation-capable environment is available for imports, tests, and image builds.
