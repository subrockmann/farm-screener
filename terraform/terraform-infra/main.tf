terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  #  credentials = 
  project = var.project
  region  = var.region
}


resource "google_storage_bucket" "raw-data-bucket" {
  name          = var.gcs_bucket_name_raw
  location      = var.region
  force_destroy = false # prevents deletion of the bucket if it is not empty

  # Optional, but recommended settings:
  storage_class               = var.gcs_storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  #   lifecycle_rule {
  #     action {
  #       type = "Delete"
  #     }
  #     condition {
  #       age = 0 #30  // days
  #     }
  #   }
}


resource "google_storage_bucket" "clean-data-bucket" {
  name          = var.gcs_bucket_name_clean
  location      = var.region
  force_destroy = false # prevents deletion of the bucket if it is not empty

  # Optional, but recommended settings:
  storage_class               = var.gcs_storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}

resource "google_bigquery_dataset" "default" {
  dataset_id = var.bq_dataset_name
  project    = var.project
  location   = var.location
}

resource "google_bigquery_table" "offers" {
  dataset_id          = google_bigquery_dataset.default.dataset_id
  table_id            = var.bq_dataset_table_name_offers
  deletion_protection = true

  #   time_partitioning {
  #     type = "DAY"
  #   }

  labels = {
    env = "default"
  }

}
resource "google_bigquery_table" "farms" {
  dataset_id          = google_bigquery_dataset.default.dataset_id
  table_id            = var.bq_dataset_table_name_farms
  deletion_protection = true

  labels = {
    env = "default"
  }
}
