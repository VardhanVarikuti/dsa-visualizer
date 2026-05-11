provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "dsa_visualizer_sg" {
  name        = "dsa-sg"
  description = "Security group for DSA Visualizer DevOps Project"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6080
    to_port     = 6080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30080
    to_port     = 30080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "dsa-sg"
  }
}

resource "aws_instance" "dsa_visualizer_server" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.dsa_visualizer_sg.id]

  tags = {
    Name = "dsa-visualizer-devops"
  }

  user_data = <<-EOF
              #!/bin/bash

              apt update -y
              apt install -y docker.io curl unzip

              systemctl start docker
              systemctl enable docker

              usermod -aG docker ubuntu
              EOF
}