variable "aws_access_key" {
  description = "value of AWS_ACCESS_KEY_ID"
  type        = string
  default     = "localstack"
}

variable "aws_secret_key" {
  description = "value of AWS SECRET_ACCESS_KEY"
  type        = string
  default     = "localstack"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain name for Route53"
  type        = string
  default     = "bab.local"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_name" {
  description = "Name tag for VPC"
  type        = string
  default     = "bab-vpc"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "local"
}

variable "ip_whitelist" {
  description = "List of allowed IP addresses"
  type        = list(string)
  default     = ["10.0.0.0/16", "127.0.0.1/32"]
}

variable "db_name" {
  description = "Aurora database name"
  type        = string
  default     = "bab"
}

variable "db_username" {
  description = "Aurora database username"
  type        = string
  default     = "bab"
}

variable "db_password" {
  description = "Aurora database password"
  type        = string
  sensitive   = true
  default     = "development-password"
}

variable "backup_bucket_name" {
  description = "S3 bucket name for backups"
  type        = string
  default     = "bab.localstack.backups"
}
