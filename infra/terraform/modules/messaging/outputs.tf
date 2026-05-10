output "ranking_log_topic" {
  value = google_pubsub_topic.ranking_log
}

output "search_feedback_topic" {
  value = google_pubsub_topic.search_feedback
}

output "retrain_trigger_topic" {
  value = google_pubsub_topic.retrain_trigger
}

output "search_events_topic" {
  value = google_pubsub_topic.search_events
}

output "search_impressions_topic" {
  value = google_pubsub_topic.search_impressions
}

output "user_actions_topic" {
  value = google_pubsub_topic.user_actions
}
