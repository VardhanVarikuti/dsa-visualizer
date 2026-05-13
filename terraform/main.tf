provider "aws" {
  region = var.aws_region
}

# --- Security Group Configuration ---
# This security group defines the firewall rules for our DevOps server.
# We use fixed NodePorts (30000-32767 range) in Kubernetes to expose our tools 
# consistently without needing an external Load Balancer (saving costs in a dev environment).
resource "aws_security_group" "dsa_visualizer_sg" {
  name        = "dsa-sg"
  description = "Security group for DSA Visualizer DevOps Project"

  # Port 22: SSH Access for remote management
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH Access"
  }

  # Port 30080: DSA Visualizer UI (noVNC)
  # Mapped via Kubernetes NodePort for browser access
  ingress {
    from_port   = 30080
    to_port     = 30080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "DSA Visualizer noVNC UI"
  }

  # Port 30000: Jenkins Master
  # Exposing Jenkins UI via fixed NodePort
  ingress {
    from_port   = 30000
    to_port     = 30000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Jenkins UI (NodePort)"
  }

  # Port 30001: Grafana Dashboard
  # Visualization tool for cluster metrics
  ingress {
    from_port   = 30001
    to_port     = 30001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Grafana Dashboard (NodePort)"
  }

  # Port 30002: Prometheus Server
  # Metric collection and monitoring
  ingress {
    from_port   = 30002
    to_port     = 30002
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Prometheus Server (NodePort)"
  }

  # Port 6443: Kubernetes API Server
  # Allows remote kubectl management from local machine
  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "K8s API Server"
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  tags = {
    Name = "dsa-sg"
  }
}

# --- EC2 Instance Configuration ---
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

# --- Elastic IP Configuration ---
# We use an Elastic IP to ensure the public IP address remains static.
# This prevents our Jenkins, Grafana, and Visualizer URLs from changing 
# every time the instance is stopped or restarted.
resource "aws_eip" "dsa_eip" {
  instance = aws_instance.dsa_visualizer_server.id
  domain   = "vpc"

  tags = {
    Name = "dsa-visualizer-eip"
  }
}

# Associate the Elastic IP with the EC2 instance
resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.dsa_visualizer_server.id
  allocation_id = aws_eip.dsa_eip.id
}