terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.14.1"
    }
    local = {
      source = "hashicorp/local"
      version = "2.6.1"
    }
  }
}

provider "local" {}

provider "google" {
  project = var.project_id
  region  = var.region
}