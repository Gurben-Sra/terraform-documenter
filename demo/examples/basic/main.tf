module "network" {
  source = "../.."

  name               = "demo"
  availability_zone  = "us-east-1a"
}

output "vpc_id" {
  value = module.network.vpc_id
}