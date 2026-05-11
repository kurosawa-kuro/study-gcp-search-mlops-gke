# =========================================================================
# dns module (M-Wave9) — public domain serving for the search-api Gateway.
#
# Owns:
#   1. A reserved **global external IP** for the GKE Gateway
#      (gke-l7-global-external-managed). Reserving it up front means the A
#      record value is known at plan time — no chicken-and-egg with the LB.
#   2. The apex **A record** (public_domain → that IP).
#   3. **Certificate Manager** managed certificate via **DNS-01** authorization
#      (so the cert can validate before the A record propagates / before the LB
#      front-end exists), wired into a certificate-map the Gateway consumes via
#      the `networking.gke.io/certmap` annotation. Classic
#      `google_compute_managed_ssl_certificate` + `pre-shared-certs` is an
#      *Ingress*-only path and does not work with the Gateway API.
#
# Does NOT own: the Cloud DNS managed zone itself. The zone is created
# out-of-band (console) — registering a `.dev` domain via Cloud Domains
# auto-delegates the NS to Cloud DNS — so this module reads it via data source
# and only manages record-sets inside it.
# =========================================================================

data "google_dns_managed_zone" "public" {
  name    = var.dns_zone_name
  project = var.project_id
}

# --- 1. Reserved global external IP for the GKE Gateway -------------------
resource "google_compute_global_address" "search_api" {
  name    = var.gateway_ip_name
  project = var.project_id
  # address_type defaults to EXTERNAL; this is an L7 global anycast IP suitable
  # for the gke-l7-global-external-managed Gateway class.
}

# --- 2. Apex A record ----------------------------------------------------
resource "google_dns_record_set" "apex_a" {
  name         = "${var.public_domain}."
  type         = "A"
  ttl          = var.record_ttl_seconds
  managed_zone = data.google_dns_managed_zone.public.name
  project      = var.project_id
  rrdatas      = [google_compute_global_address.search_api.address]
}

# --- 3. Certificate Manager (DNS-01) ------------------------------------
resource "google_certificate_manager_dns_authorization" "search_api" {
  name        = var.dns_authorization_name
  project     = var.project_id
  location    = "global"
  domain      = var.public_domain
  description = "DNS-01 authorization for ${var.public_domain} (search-api Gateway TLS)"
}

# The CNAME record the DNS authorization requires (Certificate Manager fills in
# name/type/data; we just publish it in the zone).
resource "google_dns_record_set" "cert_auth_cname" {
  name         = google_certificate_manager_dns_authorization.search_api.dns_resource_record[0].name
  type         = google_certificate_manager_dns_authorization.search_api.dns_resource_record[0].type
  ttl          = var.record_ttl_seconds
  managed_zone = data.google_dns_managed_zone.public.name
  project      = var.project_id
  rrdatas      = [google_certificate_manager_dns_authorization.search_api.dns_resource_record[0].data]
}

resource "google_certificate_manager_certificate" "search_api" {
  name        = var.certificate_name
  project     = var.project_id
  location    = "global"
  description = "Google-managed certificate for ${var.public_domain}"

  managed {
    domains = [var.public_domain]
    dns_authorizations = [
      google_certificate_manager_dns_authorization.search_api.id,
    ]
  }
}

resource "google_certificate_manager_certificate_map" "search_api" {
  name        = var.certificate_map_name
  project     = var.project_id
  description = "Certificate map for the search-api Gateway (consumed via networking.gke.io/certmap)"
}

resource "google_certificate_manager_certificate_map_entry" "search_api" {
  name         = "${var.certificate_map_name}-entry"
  project      = var.project_id
  map          = google_certificate_manager_certificate_map.search_api.name
  certificates = [google_certificate_manager_certificate.search_api.id]
  hostname     = var.public_domain
}
