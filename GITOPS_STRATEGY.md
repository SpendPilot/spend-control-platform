# GitOps Strategy

Last updated: 2026-06-16

## Target Layout

```txt
repos/spendpilot-gitops/
  environments/
    dev/
      applications/
      values/
    staging/
      applications/
      values/
    prod/
      applications/
      values/
```

## ArgoCD Setup

- one ArgoCD instance per AKS cluster unless operations later justify centralization
- Terraform may bootstrap ArgoCD, but application rollout belongs to ArgoCD

## Application Layout

- prefer app-of-apps or a small environment application set
- one application for the SpendPilot chart per environment
- optional supporting applications for platform add-ons if later separated

## Sync Strategy

- dev: auto-sync acceptable
- staging: controlled sync or gated auto-sync
- prod: manual sync/approval

## Image Tag Update Flow

- CI publishes immutable image tags
- values or application manifests are updated through promotion PRs

## Promotion Flow

1. build and publish image
2. update dev values
3. validate in dev
4. promote same immutable tag to staging
5. promote same immutable tag to prod after approval

## Rollback Flow

- ArgoCD rollback by reverting the Git change to the previous known-good tag/config
