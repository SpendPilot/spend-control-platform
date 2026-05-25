output "resource_group_name" {
  value = module.resource_group.name
}

output "application_gateway_public_ip" {
  value = module.app_gateway.public_ip_address
}

output "application_gateway_id" {
  value = module.app_gateway.id
}

output "nat_gateway_public_ip" {
  value = azurerm_public_ip.nat_gateway.ip_address
}

output "frontend_scale_set_name" {
  value = module.frontend_vmss.name
}

output "backend_scale_set_name" {
  value = module.backend_vmss.name
}

output "data_ai_scale_set_name" {
  value = module.data_ai_vmss.name
}

output "postgres_server_name" {
  value = module.postgres.server_name
}

output "postgres_fqdn" {
  value = module.postgres.fqdn
}

output "postgres_database_name" {
  value = module.postgres.database_name
}

output "ollama_private_load_balancer_ip" {
  value = var.ollama_lb_private_ip
}
