#!/bin/bash

# CAMA-MED Pipeline Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Install Docker (if not already installed)
# Uncomment these lines if Docker is not installed on your system
# sudo apt-get update
# sudo apt-get install -y docker.io
# sudo systemctl start docker
# sudo systemctl enable docker

## Pull the CAMA-MED Docker image
docker pull camamed/camamed_pipeline_db

## Verify the installation
echo "Verifying CAMA-MED pipeline installation..."
sudo docker images | grep camamed/camamed_pipeline

## Example run command (commented out)
# Uncomment and modify this section when you know how to run the pipeline
# sudo docker run -v /path/to/input/data:/input -v /path/to/output:/output camamed/camamed_pipeline [command]

echo "CAMA-MED pipeline installation completed successfully"
