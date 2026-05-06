resource "kubernetes_namespace" "elastic_system" {
  metadata {
    name = var.elastic_system_namespace
    labels = {
      "app.kubernetes.io/part-of" = "hybrid-search"
    }
  }
}

resource "helm_release" "eck_operator" {
  name       = "eck-operator"
  namespace  = kubernetes_namespace.elastic_system.metadata[0].name
  repository = "https://helm.elastic.co"
  chart      = "eck-operator"

  version = var.eck_chart_version != "" ? var.eck_chart_version : null
}
