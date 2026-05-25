# Replace the password and restrict SSH CIDRs before running `terraform apply`.
prefix              = "spendpilot"
environment         = "prod"
location            = "Central India"
resource_group_name = "spendpilot-rg"

# Azure tags applied to all resources in this stack.
tags = {
  owner   = "platform-team"
  project = "spend-control"
}

# VM administrator settings.
admin_username      = "lijaz"
admin_password      = "Lijazsalim@2020"
admin_allowed_cidrs = []

# Network topology.
vnet_cidr            = "10.60.0.0/16"
appgw_subnet_cidr    = "10.60.0.0/24"
frontend_subnet_cidr = "10.60.10.0/24"
backend_subnet_cidr  = "10.60.20.0/24"
db_subnet_cidr       = "10.60.30.0/24"
frontend_private_ip  = "10.60.10.4"
backend_private_ip   = "10.60.20.4"
data_private_ip      = "10.60.30.4"

# Availability zones used when creating the three VMs.
zones = ["1", "2", "3"]

# VM sizing.
frontend_vm_size = "Standard_D2s_v3"
backend_vm_size  = "Standard_D2s_v3"
data_vm_size     = "Standard_D2ads_v6"

# App Gateway autoscaling and routing edge.
app_gateway_min_capacity = 2
app_gateway_max_capacity = 6

# Repository bootstrap for frontend/backend VM startup.
bootstrap_repo_owner  = "SpendPilot"
bootstrap_repo_branch = "main"
jwt_secret_key        = "dev-secret-change-me"

# Self-hosted PostgreSQL container on the data VM.
postgres_container_image = "postgres:16"
postgres_database_name   = "spend_control"
postgres_app_username    = "spendpilot"
postgres_app_password    = "spendpilot"
postgres_port            = 5432

# Ollama on the data VM.
ollama_container_image = "ollama/ollama:latest"
ollama_model           = "llama3.2"
ollama_port            = 11434
