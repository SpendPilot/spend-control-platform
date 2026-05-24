output "resource_group_name" {
  value = module.resource_group.name
}

output "application_gateway_public_ip" {
  value = module.app_gateway.public_ip_address
}

output "application_gateway_id" {
  value = module.app_gateway.id
}

output "frontend_vm_names" {
  value = module.frontend_vms.vm_names
}

output "backend_vm_names" {
  value = module.backend_vms.vm_names
}

output "data_vm_names" {
  value = module.data_vms.vm_names
}

output "acr_login_server" {
  value = module.container_registry.login_server
}
