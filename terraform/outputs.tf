output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.dsa_visualizer_server.public_ip
}
