terraform {
   backend "s3" {
    bucket = "bsb4018-s3-job-rec-backend-bucket"
    key    = "terraform.tfstate"
    region = "ap-south-1"
  }
  required_providers {
    random = {
      source = "hashicorp/random"
      version = "3.4.3"
    }
    aws = {
      source = "hashicorp/aws"
      version = "4.45.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "job_rec_model" {
  source = "./job_rec_model_bucket"
}

module "job_rec_ecr" {
  source = "./job_rec_ecr"
}

module "job_rec_ec2" {
  source = "./job_rec_ec2"
}
