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
    "frontend-subnet" = {
      address_prefixes = [var.frontend_subnet_cidr]
    }
    "backend-subnet" = {
      address_prefixes = [var.backend_subnet_cidr]
    }
    "data-ai-subnet" = {
      address_prefixes = [var.data_ai_subnet_cidr]
    }
    "postgres-subnet" = {
      address_prefixes   = [var.postgres_subnet_cidr]
      delegation_service = "Microsoft.DBforPostgreSQL/flexibleServers"
    }
  }
}

module "frontend_subnet_nsg" {
  source = "./modules/subnet-nsg"

  name                = "${local.name}-frontend-nsg"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.network.subnet_ids["frontend-subnet"]
  tags                = local.tags

  rules = concat(
    [
      {
        name                       = "allow-appgw-to-frontend"
        priority                   = 100
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "3000"
        source_address_prefix      = var.appgw_subnet_cidr
        destination_address_prefix = "*"
      }
    ],
    length(var.admin_allowed_cidrs) == 0 ? [] : [
      {
        name                       = "allow-ssh-admin"
        priority                   = 120
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefixes    = var.admin_allowed_cidrs
        destination_address_prefix = "*"
      }
    ],
  )
}

module "backend_subnet_nsg" {
  source = "./modules/subnet-nsg"

  name                = "${local.name}-backend-nsg"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.network.subnet_ids["backend-subnet"]
  tags                = local.tags

  rules = concat(
    [
      {
        name                       = "allow-appgw-to-api"
        priority                   = 100
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "8000"
        source_address_prefix      = var.appgw_subnet_cidr
        destination_address_prefix = "*"
      }
    ],
    length(var.admin_allowed_cidrs) == 0 ? [] : [
      {
        name                       = "allow-ssh-admin"
        priority                   = 120
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefixes    = var.admin_allowed_cidrs
        destination_address_prefix = "*"
      }
    ],
  )
}

module "data_ai_subnet_nsg" {
  source = "./modules/subnet-nsg"

  name                = "${local.name}-data-ai-nsg"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.network.subnet_ids["data-ai-subnet"]
  tags                = local.tags

  rules = concat(
    [
      {
        name                       = "allow-backend-to-ollama"
        priority                   = 100
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = tostring(var.ollama_port)
        source_address_prefix      = var.backend_subnet_cidr
        destination_address_prefix = "*"
      }
    ],
    length(var.admin_allowed_cidrs) == 0 ? [] : [
      {
        name                       = "allow-ssh-admin"
        priority                   = 120
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefixes    = var.admin_allowed_cidrs
        destination_address_prefix = "*"
      }
    ],
  )
}

module "app_gateway" {
  source = "./modules/app-gateway-vm-edge"

  name                = "${local.name}-appgw"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  subnet_id           = module.network.subnet_ids["appgw-subnet"]
  min_capacity        = var.app_gateway_min_capacity
  max_capacity        = var.app_gateway_max_capacity
  tags                = local.tags
}

module "postgres" {
  source = "./modules/postgres-flex"

  name                   = local.postgres_server_name
  resource_group_name    = module.resource_group.name
  location               = module.resource_group.location
  server_version         = var.postgres_version
  delegated_subnet_id    = module.network.subnet_ids["postgres-subnet"]
  virtual_network_id     = module.network.virtual_network_id
  private_dns_zone_name  = local.postgres_private_dns_zone
  administrator_login    = var.postgres_app_username
  administrator_password = var.postgres_app_password
  storage_mb             = var.postgres_storage_mb
  sku_name               = var.postgres_sku_name
  backup_retention_days  = var.postgres_backup_retention_days
  zone                   = var.postgres_zone
  ha_mode                = var.postgres_ha_mode
  ha_standby_zone        = var.postgres_ha_standby_zone
  database_name          = var.postgres_database_name
  tags                   = local.tags
}

resource "azurerm_lb" "ollama_private" {
  name                = "${local.name}-ollama-ilb"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  sku                 = "Standard"
  tags                = local.tags

  frontend_ip_configuration {
    name                          = "private-frontend"
    subnet_id                     = module.network.subnet_ids["data-ai-subnet"]
    private_ip_address_allocation = "Static"
    private_ip_address            = var.ollama_lb_private_ip
  }
}

resource "azurerm_lb_backend_address_pool" "ollama_private" {
  name            = "ollama-backend-pool"
  loadbalancer_id = azurerm_lb.ollama_private.id
}

resource "azurerm_lb_probe" "ollama_private" {
  name            = "ollama-tcp-probe"
  loadbalancer_id = azurerm_lb.ollama_private.id
  protocol        = "Tcp"
  port            = var.ollama_port
}

resource "azurerm_lb_rule" "ollama_private" {
  name                           = "ollama-rule"
  loadbalancer_id                = azurerm_lb.ollama_private.id
  protocol                       = "Tcp"
  frontend_port                  = var.ollama_port
  backend_port                   = var.ollama_port
  frontend_ip_configuration_name = "private-frontend"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.ollama_private.id]
  probe_id                       = azurerm_lb_probe.ollama_private.id
}

module "frontend_vmss" {
  source = "./modules/linux-vmss-group"

  name                                 = local.frontend_scale_set_name
  resource_group_name                  = module.resource_group.name
  location                             = module.resource_group.location
  subnet_id                            = module.network.subnet_ids["frontend-subnet"]
  vm_size                              = var.frontend_vm_size
  min_instances                        = var.frontend_vmss_min_instances
  max_instances                        = var.frontend_vmss_max_instances
  admin_username                       = var.admin_username
  admin_password                       = var.admin_password
  zones                                = var.zones
  node_role                            = "frontend"
  bootstrap_repo_owner                 = var.bootstrap_repo_owner
  bootstrap_repo_branch                = var.bootstrap_repo_branch
  bootstrap_app_env                    = "development"
  bootstrap_public_api_base_url        = local.frontend_public_api_base_url
  bootstrap_public_base_url            = "http://${module.app_gateway.public_ip_address}"
  bootstrap_jwt_secret_key             = var.jwt_secret_key
  application_gateway_backend_pool_ids = [module.app_gateway.backend_pool_ids.frontend]
  tags                                 = local.tags
}

module "backend_vmss" {
  source = "./modules/linux-vmss-group"

  name                                 = local.backend_scale_set_name
  resource_group_name                  = module.resource_group.name
  location                             = module.resource_group.location
  subnet_id                            = module.network.subnet_ids["backend-subnet"]
  vm_size                              = var.backend_vm_size
  min_instances                        = var.backend_vmss_min_instances
  max_instances                        = var.backend_vmss_max_instances
  admin_username                       = var.admin_username
  admin_password                       = var.admin_password
  zones                                = var.zones
  node_role                            = "backend"
  bootstrap_repo_owner                 = var.bootstrap_repo_owner
  bootstrap_repo_branch                = var.bootstrap_repo_branch
  bootstrap_app_env                    = var.environment == "prod" ? "production" : var.environment
  bootstrap_public_base_url            = "http://${module.app_gateway.public_ip_address}"
  bootstrap_database_url               = local.backend_database_url
  bootstrap_database_host              = local.backend_database_host
  bootstrap_database_port              = 5432
  bootstrap_ollama_base_url            = local.ollama_private_base_url
  bootstrap_jwt_secret_key             = var.jwt_secret_key
  bootstrap_expense_service_url        = "http://expense-service:8001"
  bootstrap_ai_service_url             = "http://ai-service:8002"
  bootstrap_receipt_threshold          = 75
  bootstrap_upload_dir                 = "/data/uploads"
  bootstrap_ollama_timeout             = 30
  application_gateway_backend_pool_ids = [module.app_gateway.backend_pool_ids.api]
  tags                                 = local.tags
}

module "data_ai_vmss" {
  source = "./modules/linux-vmss-group"

  name                                   = local.data_ai_scale_set_name
  resource_group_name                    = module.resource_group.name
  location                               = module.resource_group.location
  subnet_id                              = module.network.subnet_ids["data-ai-subnet"]
  vm_size                                = var.data_vm_size
  min_instances                          = var.data_ai_vmss_min_instances
  max_instances                          = var.data_ai_vmss_max_instances
  admin_username                         = var.admin_username
  admin_password                         = var.admin_password
  zones                                  = var.zones
  node_role                              = "data-ai"
  ollama_enabled                         = true
  ollama_image                           = var.ollama_container_image
  ollama_model                           = var.ollama_model
  ollama_port                            = var.ollama_port
  bootstrap_repo_owner                   = var.bootstrap_repo_owner
  bootstrap_repo_branch                  = var.bootstrap_repo_branch
  bootstrap_app_env                      = var.environment == "prod" ? "production" : var.environment
  bootstrap_public_base_url              = "http://${module.app_gateway.public_ip_address}"
  bootstrap_jwt_secret_key               = var.jwt_secret_key
  load_balancer_backend_address_pool_ids = [azurerm_lb_backend_address_pool.ollama_private.id]
  tags                                   = local.tags
}
