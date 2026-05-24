module "resource_group" {
  source = "./modules/resource-group"

  name     = local.rg_name
  location = var.location
  tags     = local.tags
}

module "log_analytics" {
  source = "./modules/log-analytics"

  name                = "${local.name}-law"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  tags                = local.tags
}

module "container_registry" {
  source = "./modules/container-registry"

  name                = replace(substr("${local.name}acr001", 0, 50), "-", "")
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  sku                 = var.acr_sku
  tags                = local.tags
}

module "network" {
  source = "./modules/network"

  name                = "${local.name}-vnet"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  address_space       = [var.vnet_cidr]
  tags                = local.tags

  subnets = {
    "appgw-subnet" = {
      address_prefixes = [var.appgw_subnet_cidr]
    }
    "aks-system-subnet" = {
      address_prefixes = [var.aks_system_subnet_cidr]
    }
    "aks-frontend-subnet" = {
      address_prefixes = [var.aks_frontend_subnet_cidr]
    }
    "aks-backend-subnet" = {
      address_prefixes = [var.aks_backend_subnet_cidr]
    }
    "db-subnet" = {
      address_prefixes   = [var.db_subnet_cidr]
      delegation_name    = "postgres-flex"
      delegation_service = "Microsoft.DBforPostgreSQL/flexibleServers"
    }
  }
}

module "postgres" {
  source = "./modules/postgres-flex"

  name                   = "${local.name}-pgsql"
  resource_group_name    = module.resource_group.name
  location               = module.resource_group.location
  server_version         = var.postgres_version
  delegated_subnet_id    = module.network.subnet_ids["db-subnet"]
  virtual_network_id     = module.network.virtual_network_id
  private_dns_zone_name  = "${local.name}.postgres.database.azure.com"
  administrator_login    = var.postgres_admin_login
  administrator_password = var.postgres_admin_password
  storage_mb             = var.postgres_storage_mb
  sku_name               = var.postgres_sku_name
  database_name          = var.postgres_database_name
  tags                   = local.tags
}

module "app_gateway" {
  source = "./modules/app-gateway-aks-edge"

  name                = "${local.name}-appgw"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  subnet_id           = module.network.subnet_ids["appgw-subnet"]
  min_capacity        = var.app_gateway_min_capacity
  max_capacity        = var.app_gateway_max_capacity
  tags                = local.tags
}

module "aks_cluster" {
  source = "./modules/aks-cluster"

  name                       = "${local.name}-aks"
  location                   = module.resource_group.location
  resource_group_name        = module.resource_group.name
  dns_prefix                 = "${local.name}-dns"
  kubernetes_version         = var.kubernetes_version
  private_cluster_enabled    = var.private_cluster_enabled
  authorized_ip_ranges       = var.authorized_ip_ranges
  log_analytics_workspace_id = module.log_analytics.id
  application_gateway_id     = module.app_gateway.id
  system_subnet_id           = module.network.subnet_ids["aks-system-subnet"]
  frontend_subnet_id         = module.network.subnet_ids["aks-frontend-subnet"]
  backend_subnet_id          = module.network.subnet_ids["aks-backend-subnet"]
  system_node_vm_size        = var.system_node_vm_size
  system_node_min_count      = var.system_node_min_count
  system_node_max_count      = var.system_node_max_count
  frontend_node_vm_size      = var.frontend_node_vm_size
  frontend_node_min_count    = var.frontend_node_min_count
  frontend_node_max_count    = var.frontend_node_max_count
  backend_node_vm_size       = var.backend_node_vm_size
  backend_node_min_count     = var.backend_node_min_count
  backend_node_max_count     = var.backend_node_max_count
  node_resource_group_name   = var.aks_node_resource_group_name
  service_cidr               = var.service_cidr
  dns_service_ip             = var.dns_service_ip
  tags                       = local.tags
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = module.container_registry.id
  role_definition_name = "AcrPull"
  principal_id         = module.aks_cluster.kubelet_object_id
}
