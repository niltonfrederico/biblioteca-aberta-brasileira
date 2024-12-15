variable "environment" {
  description = "Environment name"
  type        = string
  default     = "local"
}

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

variable "domain" {
  description = "Domain name"
  type        = string
  default     = "kuresto.dev.br"
}

variable "domain_ip" {
  description = "Domain IP"
  type        = string
  default     = "localhost"
}
