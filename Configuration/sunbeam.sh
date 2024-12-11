#!/bin/bash

# Sunbeam Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Download Sunbeam
wget https://github.com/sunbeam-labs/sunbeam/releases/latest/download/sunbeam.tar.gz

## Create directory and extract Sunbeam
mkdir sunbeam4.0.0
tar -zxf sunbeam.tar.gz -C sunbeam4.0.0

## Change to Sunbeam directory and run installation script
cd sunbeam4.0.0 && ./install.sh

## Activate Sunbeam environment
source activate sunbeam4.7.0

## Run tests
pytest tests/

## Provide usage instructions
echo "
Sunbeam installation completed successfully.

For more information and specific usage instructions, refer to the Sunbeam documentation:
https://sunbeam.readthedocs.io/
"




