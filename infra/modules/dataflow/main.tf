resource "google_dataflow_flex_template_job" "this" {
  provider                = google-beta
  project                 = var.project_id
  name                    = var.dataflow_template_job_name
  container_spec_gcs_path = "gs://${var.dataflow_container_spec_gcs_path}/templates/streaming-pipeline.json"
  region                = var.region
  on_delete = "drain" 

  parameters = {
    inputSubscription = var.input_subscription
  }

  max_workers             = 1
  # service_account_email   = var.dataflow_service_account
  # subnetwork              = var.vpc_subnetwork_self_link
  enable_streaming_engine = true
}