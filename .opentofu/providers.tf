# Main provider configuration
provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.aws_region

  # LocalStack endpoint configuration
  endpoints {
    apigateway = "https://localhost.localstack.cloud:4566"
    lambda     = "https://localhost.localstack.cloud:4566"
    s3         = "https://localhost.localstack.cloud:4566"
    rds        = "https://localhost.localstack.cloud:4566"
    ecr        = "https://localhost.localstack.cloud:4566"
  }

  # Skip AWS validation for local development
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  # Force path style for local development
  s3_use_path_style = true
}
