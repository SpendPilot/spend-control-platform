variable "prefix" {
  description = "Short application prefix used in Azure resource names."
  type        = string
  default     = "spendpilot"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "prod"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "Central India"
}

variable "resource_group_name" {
  description = "Primary Azure resource group name used for this AKS stack."
  type        = string
  default     = "spendpilot-prod-rg"
}

variable "aks_node_resource_group_name" {
  description = "Azure-managed AKS node resource group name. AKS requires this separate resource group for node-managed resources."
  type        = string
  default     = "spendpilot-prod-aks-nodes-rg"
}

variable "tags" {
  description = "Additional Azure tags."
  type        = map(string)
  default     = {}
}

variable "kubernetes_version" {
  description = "AKS version."
  type        = string
  default     = "1.29.9"
}

variable "private_cluster_enabled" {
  description = "Whether to create a private AKS control plane."
  type        = bool
  default     = false
}

variable "authorized_ip_ranges" {
  description = "Optional public IP ranges allowed to reach the AKS API server when the cluster is public."
  type        = list(string)
  default     = []
}

variable "vnet_cidr" {
  type    = string
  default = "10.40.0.0/16"
}

variable "appgw_subnet_cidr" {
  type    = string
  default = "10.40.0.0/24"
}

variable "aks_system_subnet_cidr" {
  type    = string
  default = "10.40.10.0/24"
}

variable "aks_frontend_subnet_cidr" {
  type    = string
  default = "10.40.20.0/24"
}

variable "aks_backend_subnet_cidr" {
  type    = string
  default = "10.40.30.0/24"
}

variable "db_subnet_cidr" {
  type    = string
  default = "10.40.40.0/24"
}

variable "service_cidr" {
  description = "Kubernetes service CIDR."
  type        = string
  default     = "10.50.0.0/16"
}

variable "dns_service_ip" {
  description = "Kubernetes DNS service IP."
  type        = string
  default     = "10.50.0.10"
}

variable "system_node_vm_size" {
  type    = string
  default = "Standard_D4ds_v5"
}

variable "system_node_min_count" {
  type    = number
  default = 1
}

variable "system_node_max_count" {
  type    = number
  default = 3
}

variable "frontend_node_vm_size" {
  type    = string
  default = "Standard_D4ds_v5"
}

variable "frontend_node_min_count" {
  type    = number
  default = 2
}

variable "frontend_node_max_count" {
  type    = number
  default = 4
}

variable "backend_node_vm_size" {
  type    = string
  default = "Standard_D8ds_v5"
}

variable "backend_node_min_count" {
  type    = number
  default = 2
}

variable "backend_node_max_count" {
  type    = number
  default = 5
}

variable "postgres_admin_login" {
  description = "PostgreSQL administrator username."
  type        = string
  default     = "spendpilotadmin"
}

variable "postgres_admin_password" {
  description = "PostgreSQL administrator password."
  type        = string
  sensitive   = true
}

variable "postgres_version" {
  type    = string
  default = "16"
}

variable "postgres_sku_name" {
  type    = string
  default = "GP_Standard_D4ds_v5"
}

variable "postgres_storage_mb" {
  type    = number
  default = 131072
}

variable "postgres_database_name" {
  type    = string
  default = "spend_control"
}

variable "app_gateway_min_capacity" {
  type    = number
  default = 2
}

variable "app_gateway_max_capacity" {
  type    = number
  default = 6
}

variable "acr_sku" {
  type    = string
  default = "Premium"
}
