#!/bin/bash

# Seeker Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone Seeker repository
git clone https://github.com/gussow/seeker.git
cd seeker

## Create and activate conda environment
conda create --name seeker python=3.7 pip -y
conda activate seeker

## Install Seeker
pip install seeker

## Verify installation
echo "Verifying Seeker installation..."
python -c "import seeker; print(f'Seeker version: {seeker.__version__}')"

## Provide usage instructions
echo "
Seeker installation completed successfully.

For more information and specific usage instructions, refer to the Seeker documentation:
https://github.com/gussow/seeker
"

## Deactivate conda environment
conda deactivate

echo "Seeker installation and configuration completed successfully"


