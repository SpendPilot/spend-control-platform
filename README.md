# Spend Control Platform

Deployment repo for the split Spend Control Console projects.

## Expected sibling repos

- `../spend-control-frontend`
- `../spend-control-control-service`
- `../spend-control-expense-service`
- `../spend-control-ai-service`

## Docker Compose

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-platform
docker compose up --build
```

## Kubernetes

Apply the manifests in `k8s/` after building and pushing the service images referenced in the YAML files.

## Smoke Test

```powershell
py -3.13 scripts/smoke_test.py
```
