# Maestro AI - Terraform Deployment Guide

## Overview

This directory contains Terraform configurations for deploying Maestro AI to various environments.

## Supported Deployment Modes

- **Local**: Deploy using Docker on your local machine
- **AWS**: Deploy to Amazon Web Services (future)
- **Azure**: Deploy to Microsoft Azure (future)

## Quick Start - Local Deployment

### Prerequisites

1. Install [Terraform](https://www.terraform.io/downloads)
2. Install [Docker](https://www.docker.com/get-started)
3. Ensure Ollama is running locally: `ollama serve`

### Deploy

```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply configuration
terraform apply

# Access the application
# Visit http://localhost:8000
```

### Environment Variables

The deployment uses these environment variables (configured via Terraform):

- `MAESTRO_LLM_BASE_URL`: Ollama API URL (default: `http://localhost:11434`)
- `MAESTRO_LLM_MODEL`: LLM model name (default: `mistral-nemo:12b`)
- `MAESTRO_API_PORT`: Application port (default: `8000`)
- `MAESTRO_DEBUG`: Debug mode (default: `false`)

### Custom Configuration

1. Copy the example variables file:

   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. Edit `terraform.tfvars` with your settings:

   ```hcl
   deployment_mode = "local"
   ollama_base_url = "http://localhost:11434"
   ollama_model    = "mistral-nemo:12b"
   app_port        = 8000
   ```

3. Apply:

   ```bash
   terraform apply
   ```

### Cleanup

```bash
terraform destroy
```

## AWS Deployment (Future)

AWS deployment will support:

- EC2 instances
- ECS containers
- Lambda functions
- RDS for data persistence

Configuration will be added in future releases.

## Azure Deployment (Future)

Azure deployment will support:

- Virtual Machines
- Container Instances
- Azure Functions
- Cosmos DB for data persistence

Configuration will be added in future releases.

## File Structure

```
terraform/
├── main.tf                      # Main Terraform configuration
├── terraform.tfvars.example     # Example variables
├── terraform.tfvars             # Your custom variables (gitignored)
└── README.md                    # This file
```

## Troubleshooting

### Docker connection issues

If Terraform can't connect to Docker:

```bash
# Linux/Mac
export DOCKER_HOST=unix:///var/run/docker.sock

# Windows
set DOCKER_HOST=npipe:////./pipe/docker_engine
```

### Port already in use

Change the port in `terraform.tfvars`:

```hcl
app_port = 8001
```

### Ollama not accessible

Ensure Ollama is running and accessible:

```bash
# Test Ollama
curl http://localhost:11434/api/tags

# If not running
ollama serve
```

## Security

- Never commit `terraform.tfvars` with sensitive data
- Use Terraform Cloud or encrypted backends for production
- Rotate secrets regularly
- Use IAM roles instead of access keys when possible

## Support

For issues or questions, please open a GitHub issue.
