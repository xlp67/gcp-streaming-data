resource "google_storage_bucket" "this" {
  name          = var.storage_bucket_name
  location      = "us-central1" 
  force_destroy = true
  uniform_bucket_level_access = true
  soft_delete_policy {
    retention_duration_seconds = 0
  }

  hierarchical_namespace {
    enabled = true
  }
}

resource "google_storage_folder" "temp" {
  bucket = google_storage_bucket.this.name
  name   = "temp/"
}
