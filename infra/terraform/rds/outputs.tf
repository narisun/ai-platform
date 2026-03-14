output "rds_endpoint" {
  description = "The connection endpoint for the AI memory database"
  value       = aws_db_instance.ai_memory.endpoint
}

output "rds_db_name" {
  description = "The name of the database"
  value       = aws_db_instance.ai_memory.db_name
}