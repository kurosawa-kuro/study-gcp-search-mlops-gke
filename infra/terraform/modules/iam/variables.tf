variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository (owner/name) trusted by Workload Identity Federation"
  type        = string
}

variable "admin_user_emails" {
  description = "Developer user account emails that need TokenCreator on sa-api for local one-off ops (OIDC impersonation). Empty list disables the binding."
  type        = list(string)
  default     = []
}
