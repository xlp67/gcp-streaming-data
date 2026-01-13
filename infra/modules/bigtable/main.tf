resource "google_bigtable_instance" "this" {
    name = var.bigtable_instance_name
    deletion_protection = false
    cluster {
        cluster_id   = var.bigtable_cluster_id
        zone         = var.bigtable_zone
        num_nodes    = var.bigtable_num_nodes
        storage_type = var.bigtable_storage_type
    }
}

resource "google_bigtable_table" "this" {
    name          = var.bigtable_table_name
    instance_name = google_bigtable_instance.this.name
    deletion_protection = "UNPROTECTED"
}