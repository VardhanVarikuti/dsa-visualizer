output "public_ip" {
  description = "Static Public IP (Elastic IP) of the DevOps server"
  value       = aws_eip.dsa_eip.public_ip
}
