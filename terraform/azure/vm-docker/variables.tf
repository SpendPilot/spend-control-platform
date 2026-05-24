variable "prefix" {
  type    = string
  default = "spendpilot"
}

variable "environment" {
  type    = string
  default = "prod"
}

variable "location" {
  type    = string
  default = "Central India"
}

variable "resource_group_name" {
  description = "Single Azure resource group name used for this entire VM deployment stack."
  type        = string
  default     = "spendpilot-prod-rg"
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "admin_username" {
  type    = string
  default = "azureuser"
}

variable "admin_password" {
  description = "Administrator password used for SSH login to the Linux virtual machines."
  type        = string
  sensitive   = true
}

variable "admin_allowed_cidrs" {
  description = "CIDRs allowed to SSH into the Linux virtual machines."
  type        = list(string)
  default     = []
}

variable "vnet_cidr" {
  type    = string
  default = "10.60.0.0/16"
}

variable "appgw_subnet_cidr" {
  type    = string
  default = "10.60.0.0/24"
}

variable "frontend_subnet_cidr" {
  type    = string
  default = "10.60.10.0/24"
}

variable "backend_subnet_cidr" {
  type    = string
  default = "10.60.20.0/24"
}

variable "db_subnet_cidr" {
  type    = string
  default = "10.60.30.0/24"
}

variable "frontend_vm_size" {
  type    = string
  default = "Standard_D4ds_v5"
}

variable "backend_vm_size" {
  type    = string
  default = "Standard_D8ds_v5"
}

variable "data_vm_size" {
  type    = string
  default = "Standard_D4ds_v5"
}

variable "postgres_container_image" {
  description = "Container image used for the self-hosted PostgreSQL service on the data VM."
  type        = string
  default     = "postgres:16"
}

variable "postgres_database_name" {
  description = "Application database name created by the PostgreSQL container."
  type        = string
  default     = "spend_control"
}

variable "postgres_app_username" {
  description = "Application database username created by the PostgreSQL container."
  type        = string
  default     = "spendpilot"
}

variable "postgres_app_password" {
  description = "Application database password used by the PostgreSQL container."
  type        = string
  sensitive   = true
}

variable "postgres_port" {
  description = "Private port exposed by PostgreSQL on the data VM."
  type        = number
  default     = 5432
}

variable "ollama_container_image" {
  description = "Container image used for the Ollama service on the data VM."
  type        = string
  default     = "ollama/ollama:latest"
}

variable "ollama_model" {
  description = "Ollama model to pull automatically on first boot."
  type        = string
  default     = "llama3.2"
}

variable "ollama_port" {
  description = "Private port exposed by Ollama on the data VM."
  type        = number
  default     = 11434
}

variable "zones" {
  type    = list(string)
  default = ["1", "2", "3"]
}

variable "acr_sku" {
  type    = string
  default = "Premium"
}

variable "app_gateway_min_capacity" {
  type    = number
  default = 2
}

variable "app_gateway_max_capacity" {
  type    = number
  default = 6
}
