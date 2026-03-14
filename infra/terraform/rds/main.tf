terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# KMS Key for Storage Encryption
resource "aws_kms_key" "rds_key" {
  description             = "KMS key for AI Platform RDS encryption"
  enable_key_rotation     = true
}

# DB Subnet Group ensures the DB is not exposed to the public internet
resource "aws_db_subnet_group" "ai_memory_subnet" {
  name       = "ai-memory-subnet-group"
  subnet_ids = var.private_subnet_ids
  tags = {
    Environment = "Dev"
    Project     = "AgenticAI"
  }
}

# Security Group for the RDS instance
resource "aws_security_group" "rds_sg" {
  name        = "ai-memory-rds-sg"
  description = "Allow inbound PostgreSQL traffic from EKS/App subnets"
  vpc_id      = var.vpc_id

  ingress {
    description = "PostgreSQL access from internal network"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"] # Adjust to your internal VPC CIDR
  }
}

# Parameter group to preload the pgvector library
resource "aws_db_parameter_group" "pgvector_params" {
  name   = "ai-memory-pg16-params"
  family = "postgres16"

  parameter {
    name  = "shared_preload_libraries"
    value = "vector"
    apply_method = "pending-reboot"
  }
}

# The actual RDS PostgreSQL Instance
resource "aws_db_instance" "ai_memory" {
  identifier                  = "ai-memory-pg"
  engine                      = "postgres"
  engine_version              = "16.3" # pgvector is natively supported in RDS PG 15+
  instance_class              = "db.t4g.medium" # ARM-based, cost-effective for dev
  allocated_storage           = 50
  max_allocated_storage       = 100
  storage_type                = "gp3"
  storage_encrypted           = true
  kms_key_id                  = aws_kms_key.rds_key.arn
  
  db_name                     = "ai_memory"
  username                    = "dbadmin"
  password                    = var.db_password
  
  db_subnet_group_name        = aws_db_subnet_group.ai_memory_subnet.name
  vpc_security_group_ids      = [aws_security_group.rds_sg.id]
  parameter_group_name        = aws_db_parameter_group.pgvector_params.name
  
  skip_final_snapshot         = true # Set to false for production
  publicly_accessible         = false
  multi_az                    = false # Set to true for production

  tags = {
    Environment = "Dev"
    Project     = "AgenticAI"
  }
}