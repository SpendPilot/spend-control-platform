locals {
  name    = lower("${var.prefix}-${var.environment}")
  rg_name = var.resource_group_name

  tags = merge(
    {
      application = "spend-control"
      environment = var.environment
      managed_by  = "terraform"
      stack       = "vm-docker"
    },
    var.tags,
  )

  frontend_scale_set_name = "${local.name}-frontend-vmss"
  backend_scale_set_name  = "${local.name}-backend-vmss"
  data_ai_scale_set_name  = "${local.name}-data-ai-vmss"

  postgres_server_name         = "${local.name}-psql"
  postgres_private_dns_zone    = "${local.name}.postgres.database.azure.com"
  backend_database_host        = module.postgres.fqdn
  backend_database_url         = "postgresql+psycopg://${var.postgres_app_username}:${var.postgres_app_password}@${local.backend_database_host}:5432/${var.postgres_database_name}?sslmode=require"
  ollama_private_base_url      = "http://${var.ollama_lb_private_ip}:${var.ollama_port}"
  frontend_public_api_base_url = ""
}
