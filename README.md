# Spend Control Platform

Deployment repo for the split Spend Control Console projects.

## Quick Start - Clone All Repositories

Use the provided clone script to set up all required repositories in one step:

### Windows (PowerShell)

```powershell
./clone-all-repos.ps1 -BaseDir "C:\path\to\projects"
```

### macOS/Linux (Bash)

```bash
./clone-all-repos.sh /path/to/projects
```

The script will clone all five repositories:
- `spend-control-platform`
- `spend-control-frontend`
- `spend-control-control-service`
- `spend-control-expense-service`
- `spend-control-ai-service`

## Expected sibling repos

- `../spend-control-frontend`
- `../spend-control-control-service`
- `../spend-control-expense-service`
- `../spend-control-ai-service`

## Docker Compose - Local Development

The platform is split into three separate Docker Compose files for better separation of concerns:

### 1. Infrastructure Services (PostgreSQL + Ollama)

Start the infrastructure services first:

```powershell
cd spend-control-platform
docker compose -f docker-compose.infrastructure.yml up --build
```

### 2. Backend Services (AI, Control, Expense Services)

In a new terminal:

```powershell
cd spend-control-platform
docker compose -f docker-compose.backend.yml up --build
```

For Azure VMSS mode on the backend scale set, use the Azure-specific env file:

```powershell
Copy-Item .env.azure-vm.backend.example .env.azure-vm.backend
# Replace <POSTGRES_FQDN>, <OLLAMA_PRIVATE_LB_IP>, and secrets first
docker compose --env-file .env.azure-vm.backend -f docker-compose.backend.yml up --build -d
```

### 3. Frontend

In another terminal:

```powershell
cd spend-control-platform
docker compose -f docker-compose.frontend.yml up --build
```

### Environment Configuration

Copy the example environment file to create your `.env` file:

```powershell
Copy-Item .env.example .env
```

All services use environment variables defined in `.env` for configuration, including:
- local PostgreSQL credentials for the local Docker Compose path
- API endpoints and CORS origins
- JWT secrets
- Ollama model configuration
- Frontend API URL via `NEXT_PUBLIC_API_BASE_URL`

## Kubernetes

Apply the manifests in `k8s/` after building and pushing the service images referenced in the YAML files.

## Azure Terraform

Two Azure infrastructure paths now live in this repo:

- `terraform/azure/aks`
- `terraform/azure/vm-docker`

Custom reusable modules live under:

- `terraform/azure/aks/modules`
- `terraform/azure/vm-docker/modules`

Recommended default:

- use `AKS` as the main production target
- keep `vm-docker` as the simpler fallback or first rollout option

Resource group behavior:

- `vm-docker` uses one primary resource group for the whole deployment
- `aks` uses one primary resource group plus an Azure-required node resource group

Read the design notes first:

- [docs/azure-infrastructure.md](/c:/Users/lijaz/Desktop/PROJECT2/spend-control-platform/docs/azure-infrastructure.md)
- [architecture.md](/c:/Users/lijaz/Desktop/PROJECT2/spend-control-platform/architecture.md)

### AKS

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-platform\terraform\azure\aks
copy terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

### Regular Azure VM Scale Sets

This path now uses three Linux VM scale sets plus Azure Database for PostgreSQL Flexible Server.

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-platform\terraform\azure\vm-docker
copy terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

To force all three VM scale sets to refresh cloud-init bootstrap with the latest repo code:

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-platform
.\scripts\rebootstrap_vm_docker_vms.ps1
```

Plan-only mode:

```powershell
.\scripts\rebootstrap_vm_docker_vms.ps1 -PlanOnly
```

What the VMSS path provisions:

- public Azure Application Gateway WAF v2
- one frontend VM scale set
- one backend VM scale set
- one data-ai VM scale set for Ollama
- Azure Database for PostgreSQL Flexible Server in a delegated subnet
- Docker-ready cloud-init on the scale set instances

Important for VMSS mode:

- `postgres` and `ollama` are Docker-local hostnames used only by the local Compose setup
- in Azure VMSS mode, the backend scale set connects to PostgreSQL Flexible Server through its private FQDN
- Ollama is exposed privately through an internal load balancer, surfaced as `ollama_private_load_balancer_ip`

Module structure:

- each deployment type owns its own `modules/` directory
- the environment roots only compose those modules with environment-specific variables

## Smoke Test

```powershell
py -3.13 scripts/smoke_test.py
```
