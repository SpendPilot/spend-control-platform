# Spend Control Platform Runbook

## Required sibling repos

- `../spend-control-frontend`
- `../spend-control-control-service`
- `../spend-control-expense-service`
- `../spend-control-ai-service`

## Quick Start - Clone All Repositories

Use the provided clone script to set up all required repositories in one command:

### Windows (PowerShell)

```powershell
.\clone-all-repos.ps1 -BaseDir "C:\path\to\projects"
```

### macOS/Linux (Bash)

```bash
./clone-all-repos.sh /path/to/projects
```

## Bring up the full stack - Separated Services

The platform is now organized into three separate Docker Compose files for modularity:

### 1. Start Infrastructure Services (PostgreSQL + Ollama)

Open a terminal and run:

```powershell
cd spend-control-platform
Copy-Item .env.example .env  # Copy environment configuration
docker compose -f docker-compose.infrastructure.yml up --build
```

Wait for both PostgreSQL and Ollama to show as healthy before proceeding.

### 2. Start Backend Services (Control, Expense, AI Services)

Open a second terminal:

```powershell
cd spend-control-platform
docker compose -f docker-compose.backend.yml up --build
```

This will start:
- expense-service (port 8001)
- ai-service (port 8002)
- control-service (port 8000)

The services will automatically run database migrations on startup.

For Azure VMSS mode on the backend scale set:

```powershell
Copy-Item .env.azure-vm.backend.example .env.azure-vm.backend
# Replace <POSTGRES_FQDN>, <OLLAMA_PRIVATE_LB_IP>, JWT secret, and DB password
docker compose --env-file .env.azure-vm.backend -f docker-compose.backend.yml up --build -d
```

### 3. Start Frontend

Open a third terminal:

```powershell
cd spend-control-platform
docker compose -f docker-compose.frontend.yml up --build
```

Access the frontend at `http://localhost:3000`

## Environment Configuration

All services use environment variables defined in `.env`. Copy `.env.example` to `.env` and adjust values as needed:

```powershell
Copy-Item .env.example .env
```

Key variables:
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Local Docker Compose database credentials
- `JWT_SECRET_KEY`: Change for production
- `OLLAMA_MODEL`: LLM model to use
- `CORS_ORIGINS`: Frontend URL for CORS
- `NEXT_PUBLIC_API_BASE_URL`: Frontend browser-to-API endpoint

## Docker Compose File Reference

### docker-compose.infrastructure.yml
- **PostgreSQL 16**: Database server on port 5432
- **Ollama**: LLM inference on port 11434
- Creates shared `spend-control-network` for service communication

### docker-compose.backend.yml
- **expense-service**: Port 8001
- **ai-service**: Port 8002, depends on Ollama
- **control-service**: Port 8000, orchestrates expense and AI services
- Services connect to PostgreSQL at `postgres:5432`
- In Azure VMSS mode, `DATABASE_URL` should point to the PostgreSQL private FQDN
- In Azure VMSS mode, `OLLAMA_BASE_URL` should point to the internal Ollama load balancer IP

### docker-compose.frontend.yml
- **Next.js Frontend**: Port 3000
- `NEXT_PUBLIC_API_BASE_URL` environment variable controls backend API endpoint

## Azure deployment paths

Use one of these Terraform roots:

- `terraform/azure/aks`
- `terraform/azure/vm-docker`

Reusable module code is under:

- `terraform/azure/aks/modules`
- `terraform/azure/vm-docker/modules`

### AKS quick flow

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-platform\terraform\azure\aks
copy terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

### Regular VMSS quick flow

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-platform\terraform\azure\vm-docker
copy terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

After apply, use the PostgreSQL FQDN and Ollama load balancer IP for backend connectivity:

```powershell
terraform output postgres_fqdn
terraform output ollama_private_load_balancer_ip
```

In Azure VMSS mode:

- `postgres` is not a valid hostname across VMs
- `ollama` is not a valid hostname across VMs
- use the PostgreSQL private FQDN and the Ollama load balancer IP in:
  - `DATABASE_URL`
  - `OLLAMA_BASE_URL`

## Current Azure recommendation

Deploy `AKS` as the long-term production target.

Use `vm-docker` if you want:

- a simpler first Azure rollout
- fewer moving parts than Kubernetes
- VM scale sets instead of Kubernetes

## Resource groups

- `vm-docker`: one primary resource group
- `aks`: one primary resource group plus one Azure-managed node resource group

The extra AKS node resource group is an Azure platform requirement, not extra app sprawl from this Terraform.

## Important app behavior note

The frontend currently calls the API from the browser. Because of that, the Azure design here uses a public edge gateway with path routing:

- `/` to frontend
- `/api/*` to `control-service`

That keeps the data tier private without breaking the current frontend behavior.

## Health endpoints

- frontend: `http://localhost:3000`
- control-service: `http://localhost:8000/health`
- expense-service: `http://localhost:8001/health`
- ai-service: `http://localhost:8002/health`
- ollama: `http://localhost:11434/api/tags`

## Common failures

### Docker daemon not running

Start Docker Desktop, then retry:

```powershell
docker version
```

### One repo is missing

Compose builds from sibling repos. If one folder is missing, recreate or clone it beside `spend-control-platform`.

### Terraform provider cache or init issues

Re-run init in the affected root:

```powershell
terraform init -upgrade
```

### Terraform validation

Both Azure roots were validated locally with:

```powershell
terraform validate
```

from:

- `terraform/azure/aks`
- `terraform/azure/vm-docker`

### Ollama unavailable

AI falls back safely, but to restore model responses:

```powershell
ollama serve
ollama pull llama3.2
```

### Verify the split setup

```powershell
py -3.13 scripts/smoke_test.py
```
