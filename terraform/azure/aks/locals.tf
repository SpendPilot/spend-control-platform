locals {
  name          = lower("${var.prefix}-${var.environment}")
  compact_name  = substr(replace(lower("${var.prefix}${var.environment}"), "-", ""), 0, 18)
  alnum_name    = replace(local.name, "-", "")
  rg_name       = var.resource_group_name
  frontend_repo = "${module.container_registry.login_server}/spend-control-frontend"
  backend_repo  = "${module.container_registry.login_server}/spend-control-backend"

  backend_audience = "api://${local.name}-api"
  frontend_host    = azurerm_cdn_frontdoor_endpoint.this.host_name
  backend_source_hash = sha256(
    join(
      ",",
      [for file in sort(fileset("${path.root}/../../../backend", "**")) : filesha256("${path.root}/../../../backend/${file}")],
    ),
  )
  frontend_source_hash = sha256(
    join(
      ",",
      [for file in sort(fileset("${path.root}/../../../frontend", "**")) : filesha256("${path.root}/../../../frontend/${file}")],
    ),
  )
  application_rollout_revision = sha256("${local.backend_source_hash}:${local.frontend_source_hash}:${var.image_tag}")
  frontend_redirect_uris = distinct(
    concat(
      var.frontend_redirect_uris,
      ["https://${azurerm_cdn_frontdoor_endpoint.this.host_name}/login"],
    )
  )
  kube_admin_config = try(yamldecode(data.azurerm_kubernetes_cluster.credentials.kube_admin_config_raw), null)

  tags = merge(
    {
      application = "spend-control"
      environment = var.environment
      managed_by  = "terraform"
      stack       = "aks"
    },
    var.tags,
  )
}
