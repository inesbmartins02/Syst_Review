#!/bin/bash

# VEBA Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone VEBA repository
git clone https://github.com/jolespin/veba.git
cd veba

## Initialize conda for bash
conda init bash

## Clean and update conda
conda clean --all -y
conda update -n base --all -y

## Install and update mamba
conda install -c conda-forge mamba -y
conda update mamba -y

## Set permissions for VEBA scripts
chmod 775 veba/bin/*.py
chmod 775 veba/bin/scripts/*
chmod 775 veba/install/*.sh

## Install VEBA
cd veba/install
bash install.sh

## Download VEBA databases
conda activate VEBA-database_env
bash download_databases.sh /path/to/veba_database/

## Provide usage instructions
echo "
VEBA installation and database download completed successfully.

For more information and detailed usage instructions, refer to the VEBA documentation:
https://github.com/jolespin/veba
"
