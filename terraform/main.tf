# Terraform configuration for Maestro AI deployment
# Supports deployment to AWS, Azure, or local Docker

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables
variable "deployment_mode" {
  description = "Deployment mode: local, aws, or azure"
  type        = string
  default     = "local"
}

variable "ollama_base_url" {
  description = "Base URL for Ollama LLM service"
  type        = string
  default     = "http://localhost:11434"
}

variable "ollama_model" {
  description = "LLM model to use"
  type        = string
  default     = "mistral-nemo:12b"
}

variable "app_port" {
  description = "Application port"
  type        = number
  default     = 8000
}

# Local Docker deployment
provider "docker" {
  count = var.deployment_mode == "local" ? 1 : 0
}

resource "docker_image" "maestro_ai" {
  count = var.deployment_mode == "local" ? 1 : 0
  name  = "maestro-ai:latest"
  
  build {
    context    = "."
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "maestro_ai" {
  count = var.deployment_mode == "local" ? 1 : 0
  name  = "maestro-ai-app"
  image = docker_image.maestro_ai[0].image_id
  
  ports {
    internal = var.app_port
    external = var.app_port
  }
  
  env = [
    "MAESTRO_LLM_BASE_URL=${var.ollama_base_url}",
    "MAESTRO_LLM_MODEL=${var.ollama_model}",
    "MAESTRO_API_PORT=${var.app_port}",
    "MAESTRO_DEBUG=false"
  ]
  
  volumes {
    host_path      = "${path.cwd}/data"
    container_path = "/app/data"
  }
  
  volumes {
    host_path      = "${path.cwd}/output"
    container_path = "/app/output"
  }
}

# AWS deployment (optional)
provider "aws" {
  count  = var.deployment_mode == "aws" ? 1 : 0
  region = "us-east-1"
}

# Azure deployment (optional)
# Add Azure provider and resources here if needed

# Outputs
output "app_url" {
  value = var.deployment_mode == "local" ? "http://localhost:${var.app_port}" : "Check cloud provider console"
}

output "deployment_mode" {
  value = var.deployment_mode
}
