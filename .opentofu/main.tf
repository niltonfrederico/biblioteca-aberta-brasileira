# Main provider configuration
provider "aws" {
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"

  # LocalStack endpoint configuration
  endpoints {
    apigateway = "http://localhost:4566"
    lambda     = "http://localhost:4566"
    s3         = "http://localhost:4566"
    route53    = "http://localhost:4566"
    rds        = "http://localhost:4566"
  }

  # Skip AWS validation for local development
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  # Force path style for local development
  s3_use_path_style = true
}

# Route53 Configuration
resource "aws_route53_zone" "main" {
  name = var.domain_name
}
