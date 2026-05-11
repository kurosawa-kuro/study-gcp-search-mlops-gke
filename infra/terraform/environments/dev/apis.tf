locals {
  required_apis = [
    "bigquery.googleapis.com",
    "bigquerystorage.googleapis.com",
    "run.googleapis.com", # Cloud Run (legacy / smoke alternates; not the canonical serving layer)
    "artifactregistry.googleapis.com",
    "aiplatform.googleapis.com",
    "dataform.googleapis.com",
    "pubsub.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "eventarc.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "notebooks.googleapis.com",
    # GKE + Gateway API + IAP + Certificate Manager + Cloud DNS (M-Wave9 public domain)
    "container.googleapis.com",
    "gkehub.googleapis.com",
    "iap.googleapis.com",
    "networkservices.googleapis.com",
    "certificatemanager.googleapis.com",
    "dns.googleapis.com",
    # PMLE: Dataflow streaming aggregates
    "dataflow.googleapis.com",
    # Cloud Composer (Managed Airflow Gen 3) — canonical orchestrator for the
    # daily_feature_refresh / retrain_orchestration / monitoring_validation DAGs.
    "composer.googleapis.com",
  ]
}

resource "google_project_service" "enabled" {
  for_each           = toset(local.required_apis)
  service            = each.value
  disable_on_destroy = false
}
