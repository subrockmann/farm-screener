variable "credentials" {
  description = "My Credentials"
  default     = "<Path to your Service Account json file>"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "farm-screener"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "europe-west3"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "EU"
}

# Google cloud storage

variable "gcs_bucket_name_raw" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "farm-screener-raw"
}

variable "gcs_bucket_name_clean" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "farm-screener-clean"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

# Google Biq Query

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "farm_screener"
}

variable "bq_dataset_table_name_offers" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "offers"
}

variable "bq_dataset_table_name_farms" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "farms"
}