variable "aws_region" {
  description = "AWS region"
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.medium"
}

variable "ami_id" {
  description = "AMI ID for Ubuntu 24.04 LTS"
  default     = "ami-0ad21ae1d0696ad58" # Ubuntu 24.04 in ap-south-1
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
}
