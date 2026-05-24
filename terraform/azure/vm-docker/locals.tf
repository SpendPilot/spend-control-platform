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

  frontend_vm_names = ["${local.name}-frontend"]
  backend_vm_names  = ["${local.name}-backend"]
  data_vm_names     = ["${local.name}-data-ai"]
}
