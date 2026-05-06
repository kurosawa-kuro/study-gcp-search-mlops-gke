output "elastic_system_namespace" {
  description = "Namespace where the ECK operator is installed."
  value       = kubernetes_namespace.elastic_system.metadata[0].name
}

output "eck_operator_release_name" {
  description = "Helm release name of the ECK operator."
  value       = helm_release.eck_operator.name
}
