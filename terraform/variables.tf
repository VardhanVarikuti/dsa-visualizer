variable "aws_region" {
  description = "AWS region"
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.medium"
}

variable "ami_id" {
  description = "AMI ID for Amazon Linux 2023"
  default     = "ami-0f5ee92e2d63afc18" # Update with actual AMI ID if needed
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
}
