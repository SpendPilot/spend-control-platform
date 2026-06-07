output "id" {
  value = azurerm_kubernetes_cluster.this.id
}

output "name" {
  value = azurerm_kubernetes_cluster.this.name
}

output "kubelet_object_id" {
  value = azurerm_kubernetes_cluster.this.kubelet_identity[0].object_id
}

output "oidc_issuer_url" {
  value = azurerm_kubernetes_cluster.this.oidc_issuer_url
}

output "host" {
  value     = one(azurerm_kubernetes_cluster.this.kube_admin_config).host
  sensitive = true
}

output "client_certificate" {
  value     = one(azurerm_kubernetes_cluster.this.kube_admin_config).client_certificate
  sensitive = true
}

output "client_key" {
  value     = one(azurerm_kubernetes_cluster.this.kube_admin_config).client_key
  sensitive = true
}

output "cluster_ca_certificate" {
  value     = one(azurerm_kubernetes_cluster.this.kube_admin_config).cluster_ca_certificate
  sensitive = true
}
