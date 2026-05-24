locals {
  name    = lower("${var.prefix}-${var.environment}")
  rg_name = var.resource_group_name

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
