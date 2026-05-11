variable "project_id" {
  description = "GCP project ID that owns the Cloud DNS zone, static IP, and Certificate Manager resources."
  type        = string
}

variable "public_domain" {
  description = "Bare public domain served by the search-api Gateway (e.g. gcp-search-mlops-gke.dev). The A record is created at the apex."
  type        = string
}

variable "dns_zone_name" {
  description = "Cloud DNS managed-zone resource name hosting public_domain. Created out-of-band (console); referenced via data source, never managed by this module."
  type        = string
}

variable "gateway_ip_name" {
  description = "Name of the reserved global external IP this module creates for the GKE Gateway. The Gateway manifest pins it via spec.addresses[].value (NamedAddress)."
  type        = string
  default     = "search-api-ip"
}

variable "certificate_name" {
  description = "Certificate Manager managed-certificate resource name."
  type        = string
  default     = "search-api-cert"
}

variable "certificate_map_name" {
  description = "Certificate Manager certificate-map resource name. The GKE Gateway references this via the networking.gke.io/certmap annotation."
  type        = string
  default     = "search-api-certmap"
}

variable "dns_authorization_name" {
  description = "Certificate Manager DNS authorization resource name (used for DNS-01 validation of the managed certificate)."
  type        = string
  default     = "search-api-dns-auth"
}

variable "record_ttl_seconds" {
  description = "TTL (seconds) for the A record and the DNS-authorization CNAME."
  type        = number
  default     = 300
}
