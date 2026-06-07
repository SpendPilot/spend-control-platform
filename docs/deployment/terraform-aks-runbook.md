# Terraform AKS Runbook

Validated in Azure on June 7, 2026 against:

- subscription `e1f5b4be-e0ba-4ccb-8708-a949458fcd83`
- region `Central India` for AKS, PostgreSQL, Storage, Document Intelligence, and Front Door
- region `East US 2` for Azure AI Foundry model hosting

This is the exact deployment path that was used to bring the environment up successfully.

## What Terraform creates

- resource group, VNet, subnets, Log Analytics, ACR
- AKS with OIDC issuer and Workload Identity enabled
- user-assigned managed identity and federated credential
- PostgreSQL Flexible Server and database
- Blob Storage and document container
- Azure AI Foundry account and model deployment
- Azure AI Document Intelligence account
- Microsoft Entra app registrations and service principals
- kGateway on AKS
- application namespace, services, Gateway, HTTPRoutes, and workloads
- Azure Front Door Premium, WAF, origin group, route, and origin

## Known live deployment choices

- AKS node pools use `Standard_D2s_v3`, not `Standard_D2s_v5`.
  The tested subscription had `0` vCPU quota for `Standard_DSv5` in `Central India`.
- Azure AI Foundry stays in `East US 2`.
  The tested `gpt-4.1-mini` pay-per-token deployment succeeded there, while the Central India probe did not.
- kGateway is installed from the vendored chart under `infra/vendor/kgateway/`.
  This avoids OCI chart pull failures in restricted networks.

## Prerequisites

1. Sign in to Azure CLI.
2. Select the correct subscription.
3. Fill `terraform/azure/aks/terraform.tfvars`.
4. Push your code branch to GitHub if you plan to use the ACR Task workaround.

Commands:

```powershell
az login
az account set --subscription <subscription-id>
cd terraform/azure/aks
terraform init
```

## Standard path

1. Run the first apply.

```powershell
terraform apply -var-file terraform.tfvars -auto-approve
```

2. If Helm or Kubernetes provider steps fail because the generated kubeconfig is missing, fetch admin credentials once and re-run apply.

```powershell
az aks get-credentials `
  --resource-group <resource-group> `
  --name <aks-name> `
  --admin `
  --file .generated-kubeconfig `
  --overwrite-existing

terraform apply -var-file terraform.tfvars -auto-approve
```

3. If local image builds fail because of SSL interception, skip local builds and use prebuilt images or ACR Tasks.

```powershell
terraform apply `
  -var-file terraform.tfvars `
  -var build_images_during_apply=false `
  -auto-approve
```

## ACR Task workaround for restricted laptops

Use this path when `az acr build` cannot reach the registry cleanly from the workstation.

1. Create the ACR tasks once.

```powershell
az acr task create `
  --registry <acr-name> `
  --name spend-control-backend-build `
  --context https://github.com/<org>/<repo>.git#<branch>:backend `
  --file Dockerfile `
  --image spend-control-backend:latest `
  --commit-trigger-enabled false `
  --pull-request-trigger-enabled false

az acr task create `
  --registry <acr-name> `
  --name spend-control-frontend-build `
  --context https://github.com/<org>/<repo>.git#<branch>:frontend `
  --file Dockerfile `
  --image spend-control-frontend:latest `
  --commit-trigger-enabled false `
  --pull-request-trigger-enabled false
```

2. Trigger both tasks.

```powershell
az acr task run --registry <acr-name> --name spend-control-backend-build
az acr task run --registry <acr-name> --name spend-control-frontend-build
```

3. Wait for both runs to succeed, then re-run Terraform with `build_images_during_apply=false`.

## Post-apply verification

Cluster checks:

```powershell
az aks command invoke -g <resource-group> -n <aks-name> --command "kubectl get pods -A"
az aks command invoke -g <resource-group> -n <aks-name> --command "kubectl get gateway,httproute,svc -n spend-control"
```

Direct gateway check:

```powershell
curl.exe -I http://<gateway-public-ip>
curl.exe http://<gateway-public-ip>/health
```

Front Door check:

```powershell
curl.exe -I https://<frontdoor-default-domain>
```

## Manual work after Terraform

Terraform does not manage these external steps:

- map `myfinagent.online` to Azure Front Door from Hostinger
- add the Front Door custom domain and validate TLS in the Azure portal
- assign customer users in their own Entra tenants after they consent to the app

## Front Door note

After a successful apply, Front Door configuration can still take time to propagate globally. During validation on June 7, 2026:

- the gateway public IP returned `200 OK` immediately
- the Front Door default hostname could still return a Front Door `404` during early propagation

Treat the direct gateway health check as the immediate truth, and re-test Front Door after propagation completes.

If the Front Door default hostname still returns the Azure-managed `404 CONFIG_NOCACHE` page after roughly 45 minutes:

- re-save the route and origin in the portal or by Terraform apply
- verify the gateway public IP still answers `200 OK`
- open an Azure support case for Front Door route propagation with the endpoint, route, and origin IDs
