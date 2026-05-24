variable "name" {
  type = string
}

variable "location" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "dns_prefix" {
  type = string
}

variable "kubernetes_version" {
  type = string
}

variable "private_cluster_enabled" {
  type = bool
}

variable "authorized_ip_ranges" {
  type    = list(string)
  default = []
}

variable "log_analytics_workspace_id" {
  type = string
}

variable "application_gateway_id" {
  type = string
}

variable "system_subnet_id" {
  type = string
}

variable "frontend_subnet_id" {
  type = string
}

variable "backend_subnet_id" {
  type = string
}

variable "system_node_vm_size" {
  type = string
}

variable "system_node_min_count" {
  type = number
}

variable "system_node_max_count" {
  type = number
}

variable "frontend_node_vm_size" {
  type = string
}

variable "frontend_node_min_count" {
  type = number
}

variable "frontend_node_max_count" {
  type = number
}

variable "backend_node_vm_size" {
  type = string
}

variable "backend_node_min_count" {
  type = number
}

variable "backend_node_max_count" {
  type = number
}

variable "node_resource_group_name" {
  type = string
}

variable "service_cidr" {
  type = string
}

variable "dns_service_ip" {
  type = string
}

variable "zones" {
  type    = list(string)
  default = ["1", "2", "3"]
}

variable "tags" {
  type    = map(string)
  default = {}
}
