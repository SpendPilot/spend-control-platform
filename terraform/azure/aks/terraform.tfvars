# Replace the password before running `terraform apply`.
prefix                       = "spendpilot"
environment                  = "prod"
location                     = "Central India"
resource_group_name          = "spendpilot-rg"
aks_node_resource_group_name = "spendpilot-aks-rg"
postgres_admin_login         = "spendpilot"
postgres_admin_password      = "postgresspass"

tags = {
  owner   = "platform-team"
  project = "spend-control"
}
