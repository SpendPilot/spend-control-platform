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
    "frontend-subnet" = {
      address_prefixes = [var.frontend_subnet_cidr]
    }
    "backend-subnet" = {
      address_prefixes = [var.backend_subnet_cidr]
    }
    "db-subnet" = {
      address_prefixes = [var.db_subnet_cidr]
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

module "db_subnet_nsg" {
  source = "./modules/subnet-nsg"

  name                = "${local.name}-db-nsg"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.network.subnet_ids["db-subnet"]
  tags                = local.tags

  rules = concat(
    [
      {
        name                       = "allow-backend-to-postgres"
        priority                   = 100
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "5432"
        source_address_prefix      = var.backend_subnet_cidr
        destination_address_prefix = "*"
      },
      {
        name                       = "allow-backend-to-ollama"
        priority                   = 110
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

module "frontend_vms" {
  source = "./modules/linux-vm-group"

  vm_names                    = local.frontend_vm_names
  resource_group_name         = module.resource_group.name
  location                    = module.resource_group.location
  subnet_id                   = module.network.subnet_ids["frontend-subnet"]
  vm_size                     = var.frontend_vm_size
  admin_username              = var.admin_username
  admin_password              = var.admin_password
  zones                       = var.zones
  node_role                   = "frontend"
  app_gateway_backend_pool_id = module.app_gateway.backend_pool_ids.frontend
  acr_id                      = module.container_registry.id
  tags                        = local.tags
}

module "backend_vms" {
  source = "./modules/linux-vm-group"

  vm_names                    = local.backend_vm_names
  resource_group_name         = module.resource_group.name
  location                    = module.resource_group.location
  subnet_id                   = module.network.subnet_ids["backend-subnet"]
  vm_size                     = var.backend_vm_size
  admin_username              = var.admin_username
  admin_password              = var.admin_password
  zones                       = var.zones
  node_role                   = "backend"
  app_gateway_backend_pool_id = module.app_gateway.backend_pool_ids.api
  acr_id                      = module.container_registry.id
  tags                        = local.tags
}

module "data_vms" {
  source = "./modules/linux-vm-group"

  vm_names            = local.data_vm_names
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  subnet_id           = module.network.subnet_ids["db-subnet"]
  vm_size             = var.data_vm_size
  admin_username      = var.admin_username
  admin_password      = var.admin_password
  zones               = var.zones
  node_role           = "data-ai"
  acr_id              = module.container_registry.id
  postgres_enabled    = true
  postgres_image      = var.postgres_container_image
  postgres_db         = var.postgres_database_name
  postgres_user       = var.postgres_app_username
  postgres_password   = var.postgres_app_password
  postgres_port       = var.postgres_port
  ollama_enabled      = true
  ollama_image        = var.ollama_container_image
  ollama_model        = var.ollama_model
  ollama_port         = var.ollama_port
  tags                = local.tags
}
