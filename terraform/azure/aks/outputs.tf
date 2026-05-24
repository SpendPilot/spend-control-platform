output "resource_group_name" {
  value = module.resource_group.name
}

output "aks_cluster_name" {
  value = module.aks_cluster.name
}

output "aks_cluster_id" {
  value = module.aks_cluster.id
}

output "app_gateway_public_ip" {
  value = module.app_gateway.public_ip_address
}

output "app_gateway_id" {
  value = module.app_gateway.id
}

output "acr_login_server" {
  value = module.container_registry.login_server
}

output "postgres_fqdn" {
  value = module.postgres.fqdn
}

output "vnet_name" {
  value = module.network.virtual_network_name
}
