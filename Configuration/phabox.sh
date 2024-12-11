#!/bin/bash

# PhaBOX2 Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Git clone
git clone https://github.com/KennthShang/PhaBOX.git
cd PhaBOX

## Create and activate conda environment
conda create -n phabox2 phabox=2.0 -c jyshang2 -c pytorch -c huggingface -c bioconda -c conda-forge -y
conda activate phabox2

## Download and extract database
wget https://github.com/KennthShang/PhaBOX/releases/download/v2.0.0/phabox_db_v2.0.0.zip
unzip phabox_db_v2.0.0.zip > /dev/null

## Verify installation
echo "Verifying PhaBOX2 installation..."
phabox2 --help

## Provide usage instructions
echo "
PhaBOX2 installation completed successfully.

To use PhaBOX2:

1. Activate the conda environment:
   conda activate phabox2

2. Run PhaBOX2:
   phabox2 [options]

For more information and specific usage instructions, refer to the PhaBOX2 documentation.
"

echo "PhaBOX2 installation and configuration completed successfully"



