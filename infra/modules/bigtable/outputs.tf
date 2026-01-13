output "bigtable_instance_name" {
  value = google_bigtable_instance.this.name
}

output "bigtable_table_name" {
  value = google_bigtable_table.this.name
}
