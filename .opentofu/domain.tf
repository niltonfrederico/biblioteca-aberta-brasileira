# Route 53
resource "aws_route53_zone" "main" {
  name = var.domain
  tags = {
    Environment = var.environment
  }
}

resource "aws_route53_record" "wwwless" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "A"
  ttl     = "300"
  records = [var.domain_ip]
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.domain}"
  type    = "A"
  ttl     = "300"
  records = [var.domain_ip]
}

resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "A"
  ttl     = "300"
  records = [var.domain_ip]
}
