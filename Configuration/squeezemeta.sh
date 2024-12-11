#!/bin/bash

# SqueezeMeta Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone SqueezeMeta repository
git clone https://github.com/jtamames/SqueezeMeta.git
cd SqueezeMeta

## Update conda and set solver
conda update -n base conda -y
conda install -n base conda-libmamba-solver -y
conda config --set solver libmamba

## Create and activate SqueezeMeta environment
conda create -n SqueezeMeta -c conda-forge -c bioconda -c anaconda -c fpusan squeezemeta=1.6 --no-channel-priority -y
conda activate SqueezeMeta

## Test installation
test_install.pl

## Download databases
# Note: Replace /path/to/database/directory with your desired database path
DB_PATH="/path/to/database/directory"
./utils/install_utils/download_databases.pl $DB_PATH

## Provide usage instructions
echo "
SqueezeMeta installation completed successfully.

For more information and specific usage instructions, refer to the SqueezeMeta documentation:
https://github.com/jtamames/SqueezeMeta
"

## Deactivate conda environment
conda deactivate

echo "SqueezeMeta installation and configuration completed successfully"



