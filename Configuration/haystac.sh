#!/bin/bash

# Haystac Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone Haystac repository
git clone https://github.com/antonisdim/haystac.git
cd haystac

## Create and activate conda environment
mamba create -c conda-forge -c bioconda -n haystac haystac -y
mamba activate haystac

## Verify installation
echo "Verifying Haystac installation..."
haystac --help

## Provide usage instructions
echo "
Haystac installation completed successfully.

To use Haystac:

1. Activate the conda environment:
   mamba activate haystac

2. Run Haystac commands:
   haystac [command] [options]

For more information and specific usage instructions, refer to the Haystac documentation:
https://haystac.readthedocs.io/

Common Haystac commands:
- haystac database: Create a Haystac database
- haystac sample: Analyze a sample
- haystac analyse: Perform analysis on Haystac results
"

## Deactivate conda environment
mamba deactivate

echo "Haystac installation and configuration completed successfully"




