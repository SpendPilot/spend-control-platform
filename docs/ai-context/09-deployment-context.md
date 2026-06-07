# Deployment context

Canonical production path:

- `terraform/azure/aks/` provisions Azure and runs Helm
- `infra/helm/business-ai-app/` defines the in-cluster application topology
- `infra/k8s/` mirrors the same shape as raw YAML

Key deployment choices:

- no Kubernetes Ingress
- Gateway API and kGateway only
- Front Door Premium with WAF as the public edge
- backend is split into `identity`, `finance`, and `documents` services on AKS
- local docker compose stays combined for simplicity
