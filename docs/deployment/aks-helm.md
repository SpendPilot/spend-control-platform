# AKS Helm Deployment

The application Helm chart deploys the full AKS runtime shape:

- frontend
- identity-service
- finance-service
- documents-service
- migration job
- Gateway and HTTPRoutes

Render:

```bash
helm template spend-control infra/helm/business-ai-app
```

Install:

```bash
helm upgrade --install spend-control infra/helm/business-ai-app \
  --namespace spend-control \
  --create-namespace \
  -f infra/helm/business-ai-app/values-prod.yaml
```

Terraform already drives this release in the AKS stack, so manual Helm is mainly for local validation and emergency operations.
