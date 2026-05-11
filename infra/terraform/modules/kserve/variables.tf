variable "kserve_version" {
  description = "KServe chart version to install via Helm"
  type        = string
  default     = "v0.14.0"
}

variable "cert_manager_version" {
  description = "cert-manager version (KServe prerequisite)"
  type        = string
  default     = "v1.15.3"
}

variable "external_secrets_chart_version" {
  description = "External Secrets Operator Helm chart version"
  type        = string
  default     = "2.2.0"
}

variable "knative_version" {
  description = "Knative Serving version (KServe Serverless mode prerequisite). Empty skips install."
  type        = string
  default     = ""
}

variable "inference_namespace" {
  description = "Namespace for KServe InferenceService resources"
  type        = string
  default     = "kserve-inference"
}

variable "search_namespace" {
  description = "Namespace for search-api workload"
  type        = string
  default     = "search"
}

variable "ksa_names" {
  description = "KSA names created in each namespace (bound to GCP SAs via Workload Identity annotation)"
  type = object({
    api              = string
    encoder          = string
    reranker         = string
    external_secrets = string
  })
}

variable "service_accounts" {
  description = "GCP service accounts (from iam module) for Workload Identity annotations"
  type        = any
}

variable "enable_self_signed_tls" {
  description = <<-EOT
    Bootstrap a self-signed TLS Secret named `search-api-tls` in the search
    namespace. Since M-Wave9 it serves only as the Gateway listener's
    `certificateRefs` placeholder (so the listener stays PROGRAMMED) — actual
    TLS is the Google-managed cert bound via the `networking.gke.io/certmap`
    annotation. Keep `true` for dev. Earlier incident: had to
    `kubectl create secret tls` by hand mid-deploy because the listener wedged
    at PROGRAMMED=False with no Secret.
  EOT
  type        = bool
  default     = true
}

variable "tls_cn" {
  description = "Common Name + DNS SAN for the self-signed placeholder cert. Should match the Gateway listener hostname (= the public domain). dev/main.tf passes `var.public_domain`."
  type        = string
  default     = "search-api.example.com"
}
