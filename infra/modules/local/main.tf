resource "null_resource" "save_env" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = <<EOT
cat <<EOF > ${path.module}/../../../.config/.env
PROJECT_ID="${var.project}"
PUBSUB_SUBSCRIPTION_NAME="${var.pubsub_subscription}"
PUBSUB_TOPIC_ID="${var.pubsub_topic}"
STORAGE_BUCKET_NAME="${var.storage_bucket}"
BIGTABLE_INSTANCE_ID="${var.bigtable_instance}"
BIGTABLE_TABLE_NAME="${var.bigtable_table}"
EOF
EOT
  }
}
