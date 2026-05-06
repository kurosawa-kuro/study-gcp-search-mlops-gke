variable "elastic_system_namespace" {
  description = "Namespace for Elastic ECK operator components."
  type        = string
  default     = "elastic-system"
}

variable "eck_chart_version" {
  description = "Optional pinned helm chart version for ECK operator. Empty uses latest."
  type        = string
  default     = ""
}
