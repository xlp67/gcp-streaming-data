resource "google_pubsub_topic" "this" {
  name = var.topic_name

  labels = {
    name = "simulator-topic"
  }
}

resource "google_pubsub_subscription" "this" {
  name  = var.subscription_name
  topic = google_pubsub_topic.this.name
}