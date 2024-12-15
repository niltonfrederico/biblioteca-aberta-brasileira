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

variable "lambda_setup" {
  description = "Lambda setup"
  type = map(object({
    log_retention = number
    memory_size   = number
    timeout       = number
  }))

  default = {
    local = {
      log_retention = 7
      memory_size   = 128
      timeout       = 3
    }
    development = {
      log_retention = 7
      memory_size   = 128
      timeout       = 3
    }
    production = {
      log_retention = 90
      memory_size   = 512
      timeout       = 10
    }
  }
}

locals {
  current_env_suffix = var.environment == "production" ? "" : "-${var.environment}"
  common_tags = {
    Environment = var.environment
    Domain      = var.domain
    ManagedBy   = "Opentofu"
  }
}
