# Shared Resource Strategy

Last updated: 2026-06-16

## Global Shared Resources

- ACR
- optional common managed identities
- optional shared DNS only where truly global

## Non-Prod Shared Resources

- Front Door for dev/staging
- non-prod WAF policy
- optional shared AI Foundry/OpenAI and Document Intelligence resources

## Environment-Specific Resources

- `dev`: runtime infra and outputs for shared Front Door origins
- `staging`: runtime infra and outputs for shared Front Door origins
- `prod`: runtime infra plus prod Front Door and prod WAF

## Dependency Flow

- `dev` and `staging` output their origin hostnames, health paths, and routing metadata
- `nonprod-shared` reads those outputs via remote state
- `nonprod-shared` owns origin groups, origins, routes, and policy associations
- `prod` owns its own Front Door directly

## Avoiding Circular Dependencies

- shared edge states read env outputs
- env states never read shared edge route resources back
- keep DNS/domain validation dependencies one-directional where possible

## Avoiding Dual State Ownership

- only one state may own each Front Door profile, endpoint, route, origin group, origin, WAF association, and policy attachment
- only one state may own each shared resource such as ACR

## Apply Order

1. `global-shared`
2. `nonprod-shared` seed
3. `dev`
4. `staging`
5. `nonprod-shared` attach env origins
6. `prod`
