# IAM Role
resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = local.common_tags
}

# Lambda functions
# Zip example lambda functions
data "archive_file" "example" {
  type        = "zip"
  source_dir  = "${path.module}/assets/lambda_example"
  output_path = "${path.module}/assets/lambda_example.zip"
}

# Admin Lambda function
resource "aws_lambda_function" "bab_admin" {
  filename         = data.archive_file.example.output_path
  function_name    = "bab-admin${local.current_env_suffix}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.handler"
  source_code_hash = data.archive_file.example.output_base64sha256
  runtime          = "python3.13"

  memory_size = var.lambda_setup[var.environment].memory_size
  timeout     = var.lambda_setup[var.environment].timeout

  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  tags = merge(local.common_tags, {
    Name = "bab-admin${local.current_env_suffix}"
  })
}

# Outbound Lambda function
resource "aws_lambda_function" "bab_outbound" {
  filename         = data.archive_file.example.output_path
  function_name    = "bab-outbound${local.current_env_suffix}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.handler"
  source_code_hash = data.archive_file.example.output_base64sha256
  runtime          = "python3.13"

  memory_size = var.lambda_setup[var.environment].memory_size
  timeout     = var.lambda_setup[var.environment].timeout

  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  tags = merge(local.common_tags, {
    Name = "bab-outbound${local.current_env_suffix}"
  })
}

# Inbound Lambda function
resource "aws_lambda_function" "bab_inbound" {
  filename         = data.archive_file.example.output_path
  function_name    = "bab-inbound${local.current_env_suffix}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.handler"
  source_code_hash = data.archive_file.example.output_base64sha256
  runtime          = "python3.13"

  memory_size = var.lambda_setup[var.environment].memory_size
  timeout     = var.lambda_setup[var.environment].timeout

  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  tags = merge(local.common_tags, {
    Name = "bab-inbound${local.current_env_suffix}"
  })
}

# Synchronize Lambda function
resource "aws_lambda_function" "bab_synchronize" {
  filename         = data.archive_file.example.output_path
  function_name    = "bab-synchronize${local.current_env_suffix}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.handler"
  source_code_hash = data.archive_file.example.output_base64sha256
  runtime          = "python3.13"

  memory_size = var.lambda_setup[var.environment].memory_size
  timeout     = var.lambda_setup[var.environment].timeout

  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  tags = merge(local.common_tags, {
    Name = "bab-synchronize${local.current_env_suffix}"
  })
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "bab_admin" {
  name              = "/aws/lambda/bab-admin${local.current_env_suffix}"
  retention_in_days = var.lambda_setup[var.environment].log_retention
  tags              = local.common_tags
}

resource "aws_cloudwatch_log_group" "bab_outbound" {
  name              = "/aws/lambda/bab-outbound${local.current_env_suffix}"
  retention_in_days = var.lambda_setup[var.environment].log_retention
  tags              = local.common_tags
}

resource "aws_cloudwatch_log_group" "bab_inbound" {
  name              = "/aws/lambda/bab-inbound${local.current_env_suffix}"
  retention_in_days = var.lambda_setup[var.environment].log_retention
  tags              = local.common_tags
}

resource "aws_cloudwatch_log_group" "bab_synchronize" {
  name              = "/aws/lambda/bab-synchronize${local.current_env_suffix}"
  retention_in_days = var.lambda_setup[var.environment].log_retention
  tags              = local.common_tags
}
