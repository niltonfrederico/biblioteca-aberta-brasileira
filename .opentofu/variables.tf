variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain name for Route53"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_name" {
  description = "Name tag for VPC"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "ip_whitelist" {
  description = "List of allowed IP addresses"
  type        = list(string)
}

variable "db_name" {
  description = "Aurora database name"
  type        = string
}

variable "db_username" {
  description = "Aurora database username"
  type        = string
}

variable "db_password" {
  description = "Aurora database password"
  type        = string
  sensitive   = true
}

variable "backup_bucket_name" {
  description = "S3 bucket name for backups"
  type        = string
}
