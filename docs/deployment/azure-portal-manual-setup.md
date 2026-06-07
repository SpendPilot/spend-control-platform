# Azure Portal Manual Setup Guide

This guide is the portal-first fallback when you do not want to rely on Terraform for the Azure control plane.

It was updated after a live deployment validation on June 7, 2026 and reflects the working topology in this repository.

## Target architecture

```txt
Azure Front Door Premium + WAF
  -> AKS public LoadBalancer service for kGateway
  -> Gateway API HTTPRoutes
      -> frontend
      -> identity-service
      -> finance-service
      -> documents-service
```

## Portal resources to create

Create these in order:

1. Resource group in `Central India`
2. Log Analytics workspace
3. Container Registry
4. Virtual network with:
   - AKS subnet
   - PostgreSQL subnet
5. User-assigned managed identity
6. PostgreSQL Flexible Server in the delegated subnet
7. Storage account and blob container
8. Azure AI Document Intelligence in `Central India`
9. Azure AI Foundry account in `East US 2`
10. AKS cluster with Workload Identity and OIDC issuer enabled
11. Azure Front Door Premium profile, endpoint, WAF policy, origin group, origin, route
12. Microsoft Entra app registrations for frontend and backend APIs

## Critical portal settings

AKS:

- Kubernetes version: use the latest supported stable version that is compatible with your chosen kGateway release
- OIDC issuer: `Enabled`
- Workload Identity: `Enabled`
- Node pools: one `system` pool and one `user` pool
- Tested working VM size in this subscription: `Standard_D2s_v3`

Managed identity:

- create one user-assigned identity for the workloads
- grant it:
  - `Storage Blob Data Contributor` on the storage account
  - `Cognitive Services User` on the Foundry account
  - `Cognitive Services User` on the Document Intelligence account

PostgreSQL:

- use private access in the delegated subnet
- keep the app connection on SSL

Foundry:

- use `East US 2` if you want the same tested path as this repo
- deploy `gpt-4.1-mini`

Front Door:

- SKU: Premium
- WAF: attach to the endpoint
- origin protocol: HTTP to the AKS gateway LoadBalancer
- health probe path: `/health`
- route pattern: `/*`

## Manual Entra setup

Create two app registrations:

1. Frontend SPA app
   - platform: Single-page application
   - redirect URIs:
     - `https://<frontdoor-domain>/login`
     - local development URI if needed

2. Backend API app
   - expose an API application ID URI
   - create app roles if you want tenant-side role assignment

Grant admin consent after both apps are configured.

## Images and registry

If the workstation cannot push images directly because of SSL inspection or Docker restrictions, use ACR Tasks from the portal or Azure CLI.

Recommended path:

1. Push the repo branch to GitHub.
2. In ACR, create one task for `backend/` and one for `frontend/`.
3. Build `spend-control-backend:latest` and `spend-control-frontend:latest`.

## In-cluster deployment

The Azure portal does not replace these Kubernetes steps. Use Cloud Shell or a trusted machine with `kubectl` and `helm`.

1. Get AKS admin credentials.
2. Install Gateway API CRDs.
3. Install the vendored kGateway chart from `infra/vendor/kgateway/`.
4. Deploy the app Helm chart from `infra/helm/business-ai-app/`.

Important:

- the application namespace must exist before the app Helm release runs
- the app chart should not also ask Helm to create the namespace
- the migration job must run as a post-install or post-upgrade hook

## Hostinger DNS work after Azure

Terraform and the portal do not control Hostinger. After Front Door is up:

1. Add `myfinagent.online` as a custom domain on Front Door.
2. Create the required DNS validation record in Hostinger.
3. Point the domain to the Front Door hostname.
4. Wait for certificate issuance and route propagation.

## Trustworthy manual checks

Use these checks after the portal build:

- AKS pods are all `Running`
- `kubectl get gateway,httproute,svc -n spend-control` shows the gateway programmed
- the gateway public IP returns `200 OK`
- the Front Door hostname returns the frontend after propagation

If Front Door keeps returning the Azure error page with `X-Cache: CONFIG_NOCACHE` for more than roughly 45 minutes while the gateway public IP is healthy, treat it as an Azure Front Door propagation issue and escalate through Azure support.
