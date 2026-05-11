output "gateway_ip_name" {
  description = "Name of the reserved global external IP — pin it in the Gateway manifest via spec.addresses[].value (type: NamedAddress)."
  value       = google_compute_global_address.search_api.name
}

output "gateway_ip_address" {
  description = "The reserved global external IP address (also the apex A record value)."
  value       = google_compute_global_address.search_api.address
}

output "certificate_map_name" {
  description = "Certificate-map name — set it on the Gateway via the networking.gke.io/certmap annotation."
  value       = google_certificate_manager_certificate_map.search_api.name
}

output "certificate_name" {
  description = "Certificate Manager managed-certificate name (poll managed.state == ACTIVE after DNS-01 validation)."
  value       = google_certificate_manager_certificate.search_api.name
}

output "public_domain" {
  description = "Echo of the served public domain (apex)."
  value       = var.public_domain
}
