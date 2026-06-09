output "resource_group_name" {
  value = module.resource_group.name
}

output "aks_cluster_name" {
  value = module.aks_cluster.name
}

output "aks_cluster_id" {
  value = module.aks_cluster.id
}

output "acr_login_server" {
  value = module.container_registry.login_server
}

output "postgres_fqdn" {
  value = module.postgres.fqdn
}

output "frontdoor_endpoint_hostname" {
  value = azurerm_cdn_frontdoor_endpoint.this.host_name
}

output "frontend_login_url" {
  value = "https://${azurerm_cdn_frontdoor_endpoint.this.host_name}/login"
}

output "backend_api_audience" {
  value = local.backend_audience
}

output "backend_api_scope" {
  value = "${local.backend_audience}/access_as_user"
}

output "frontend_client_id" {
  value = azuread_application.frontend_spa.client_id
}

output "backend_client_id" {
  value = azuread_application.backend_api.client_id
}

output "entra_admin_consent_url_template" {
  value = "https://login.microsoftonline.com/<tenant-id-or-domain>/v2.0/adminconsent?client_id=${azuread_application.frontend_spa.client_id}&scope=${urlencode("${local.backend_audience}/.default")}&redirect_uri=${urlencode("https://${azurerm_cdn_frontdoor_endpoint.this.host_name}/login")}"
}

output "workload_identity_client_id" {
  value = azurerm_user_assigned_identity.workload.client_id
}

output "storage_account_url" {
  value = azurerm_storage_account.documents.primary_blob_endpoint
}

output "document_intelligence_endpoint" {
  value = azurerm_cognitive_account.document_intelligence.endpoint
}

output "foundry_endpoint" {
  value = azurerm_cognitive_account.foundry.endpoint
}

output "github_actions_client_id" {
  value = azuread_application.github_actions.client_id
}

output "github_actions_tenant_id" {
  value = data.azurerm_client_config.current.tenant_id
}

output "github_actions_subscription_id" {
  value = data.azurerm_client_config.current.subscription_id
}
