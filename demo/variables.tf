variable "name" {
  type        = string
  description = "Prefix used for resource names and tags."
}

variable "aws_region" {
  type        = string
  description = "AWS region where the network is created."
  default     = "us-east-1"
}

variable "availability_zone" {
  type        = string
  description = "Availability zone for the public and private subnets."
}

variable "vpc_cidr" {
  type        = string
  description = "IPv4 CIDR range for the VPC."
  default     = "10.40.0.0/16"
}

variable "public_subnet_cidr" {
  type        = string
  description = "IPv4 CIDR range for the public subnet."
  default     = "10.40.1.0/24"
}

variable "private_subnet_cidr" {
  type        = string
  description = "IPv4 CIDR range for the private subnet."
  default     = "10.40.2.0/24"
}