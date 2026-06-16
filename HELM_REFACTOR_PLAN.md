# Helm Refactor Plan

Last updated: 2026-06-16

## Current Helm/Kubernetes Layout

- canonical chart: `infra/helm/business-ai-app/`
- overlapping raw manifests: `infra/k8s/`
- vendored kGateway charts: `infra/vendor/kgateway/`

## Target Chart Layout

```txt
repos/spendpilot-helm/
  charts/
    spendpilot/
      Chart.yaml
      values.yaml
      values-dev.yaml
      values-staging.yaml
      values-prod.yaml
      templates/
        frontend/
        services/
        gateway/
        httproutes/
        config/
        secrets/
```

## Values Strategy

- `values.yaml`: shared defaults
- `values-dev.yaml`, `values-staging.yaml`, `values-prod.yaml`: environment overrides

## Image Tag Strategy

- immutable tags
- chart values updated by CI/GitOps promotion flow
- no `latest` in prod

## Secrets/Config Strategy

- non-secret config in ConfigMaps/values
- secrets sourced from sealed/external secret strategy or runtime secret injection
- avoid embedding long-lived Azure secrets

## Gateway Strategy

- keep Gateway API + kGateway
- move gateway and route templates into clear subfolders inside the chart

## Validation Commands

- `helm lint`
- `helm template` with dev values
- `helm template` with staging values
- `helm template` with prod values
