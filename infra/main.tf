module "pubsub" {
  source            = "./modules/pubsub"
  topic_name        = "iot-topic"
  subscription_name = "iot-subscription"
}

module "storage" {
  source              = "./modules/storage"
  storage_bucket_name = "iot-bucket-xlp67"
}

module "bigtable" {
  source                  = "./modules/bigtable"
  bigtable_instance_name  = "iot-bigtable-instance"
  bigtable_cluster_id     = "iot-bigtable-cluster"
  bigtable_zone           = "${var.region}-a"
  bigtable_num_nodes      = 1
  bigtable_storage_type   = "SSD"
  bigtable_table_name     = "iot-data-table"
  depends_on = [ module.pubsub, module.storage ]
}

module "local" {
  source                    = "./modules/local"
  project = var.project_id
  pubsub_subscription  = module.pubsub.subscription_name
  pubsub_topic        = module.pubsub.topic_id
  storage_bucket       = module.storage.storage_bucket_name
  bigtable_instance     = module.bigtable.bigtable_instance_name
  bigtable_table      = module.bigtable.bigtable_table_name
  depends_on = [ module.bigtable ]
}

