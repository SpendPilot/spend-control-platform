# Azure Infrastructure Recommendation

## Recommendation

Use `AKS` as the primary production target and keep `vm-docker` as the lower-complexity fallback.

Why:

- you already have four separately deployable workloads
- the service boundary is clear enough for container orchestration to pay off
- future split-repo CI/CD is easier to standardize on AKS than on per-VM Docker rollout logic
- Azure-native observability, ingress, managed identity, and scaling fit the app shape well

Use `vm-docker` when:

- the team wants lower platform complexity right now
- release cadence is moderate
- you want a simpler first production environment before moving to AKS

## Resource Group Model

For the Terraform we now use a single explicit primary resource group name per stack.

- `vm-docker`: one primary resource group for the full stack
- `aks`: one primary resource group for the stack, plus one Azure-required AKS node resource group

Important:

- the VM deployment can truly live in one resource group
- AKS cannot be reduced to one total resource group because Azure creates and manages a separate node resource group
- we now expose that AKS node resource group name as an input so it is predictable instead of auto-generated

## Important Current App Constraint

The frontend currently calls `control-service` directly from the browser through `NEXT_PUBLIC_API_BASE_URL`.

That means the safest production edge for the app today is:

- public edge gateway
- `/` -> frontend
- `/api/*` -> control-service

This keeps `expense-service`, `ai-service`, and PostgreSQL private while preserving how the frontend already behaves.

## AKS Topology

- Resource group per environment
- Single VNet
- Subnets:
  - `appgw`
  - `aks-system`
  - `aks-frontend`
  - `aks-backend`
  - `db`
- Azure Application Gateway WAF v2 at the edge
- AKS cluster with:
  - system node pool
  - frontend node pool
  - backend node pool
- Azure Container Registry
- Azure Database for PostgreSQL Flexible Server in private mode
- Log Analytics workspace

## VM-Docker Topology

- Resource group per environment
- Single VNet
- Subnets:
  - `appgw`
  - `frontend`
  - `backend`
  - `data-ai`
  - `postgres`
- Azure Application Gateway WAF v2 at the edge
- One frontend Linux VM scale set
- One backend Linux VM scale set
- One data-ai Linux VM scale set for Ollama
- Azure Database for PostgreSQL Flexible Server in private mode
- Internal load balancer for private Ollama access
- Log Analytics workspace

Important networking note:

- the frontend, backend, data-ai, and PostgreSQL subnets are all inside the same VNet
- Azure routes traffic between those subnets by default unless NSGs block it
- this Terraform allows backend-subnet to reach the data-ai subnet on the Ollama port
- the hostname `postgres` only works in the local Docker Compose network, not across Azure VMs
- in VMSS mode, the backend workloads use the PostgreSQL private FQDN and the private Ollama load balancer IP

## Production Suggestions

- Put a real DNS name in front of the public edge and terminate TLS there
- Prefer Azure Container Registry for Azure-hosted runtime pulls
- Keep the PostgreSQL service private-only inside the delegated subnet
- Treat Ollama as the first thing to split to its own compute pool if inference load grows
- Add Azure Bastion or a private jump path before enabling direct SSH
- Tighten CORS to the final public hostname once DNS is fixed
- Keep the AI tier private; only `control-service` should orchestrate it

## Decision Guidance

Choose `AKS` if your priority is:

- cleaner long-term scaling
- better deployment ergonomics
- stronger future fit for multi-service operations

Choose `vm-docker` if your priority is:

- simpler first production rollout
- fewer Kubernetes operational concerns
- easier team onboarding in the short term

## What was implemented in Terraform

Both Terraform roots create the core Azure foundation:

- networking
- data tier hosting model appropriate to the selected deployment type
- observability workspace
- edge ingress resources
- compute layer for the selected deployment model

Deployment-specific modules now live beside their respective roots:

- `terraform/azure/aks/modules`
- `terraform/azure/vm-docker/modules`

The AKS root focuses on cluster infrastructure.

The VM-Docker root now focuses on three Linux VM scale sets with Docker-ready cloud-init bootstrapping:

- frontend VM scale set
- backend VM scale set
- data-ai VM scale set for Ollama
- Azure Database for PostgreSQL Flexible Server
