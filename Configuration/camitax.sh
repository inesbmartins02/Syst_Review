#!/bin/bash

# CAMITAX Installation and Configuration Script
# This script installs and configures CAMITAX (CAMI Taxonomic Classification)

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Create and activate conda environment
conda create -n camitax_env python=3 -y
conda activate camitax_env

## Clone CAMITAX repository
git clone https://github.com/CAMI-challenge/CAMITAX.git
cd CAMITAX

## Install dependencies
conda install -c conda-forge openjdk -y
conda install -c bioconda nextflow -y
conda install -c conda-forge docker -y

## Initialize CAMITAX database
# Replace /path/to/db with your desired database path
nextflow pull CAMI-challenge/CAMITAX
DB_PATH="/path/to/db"
nextflow run CAMI-challenge/CAMITAX/init.nf --db $DB_PATH

## Verify installation
echo "Verifying CAMITAX installation..."
nextflow -version
docker --version

## Return to parent directory
cd ..

## Deactivate conda environment
conda deactivate

echo "CAMITAX installation and configuration completed successfully"





