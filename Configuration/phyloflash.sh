#!/bin/bash

# phyloFlash Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone phyloFlash repository
git clone https://github.com/HRGV/phyloFlash.git
cd phyloFlash

## Configure conda channels
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict

## Create and activate conda environment
conda create -n pf phyloflash -y
conda activate pf
conda install -c bioconda barrnap
conda install -c bioconda bedtools

## Verify installation
echo "Verifying phyloFlash installation..."
phyloFlash.pl -check_env
phyloFlash.pl -help

## Download and extract database
echo "Downloading phyloFlash database..."
wget https://zenodo.org/record/7892522/files/138.1.tar.gz
tar -xzf 138.1.tar.gz

## Provide usage instructions
echo "
phyloFlash installation completed successfully.

For more information and specific usage instructions, refer to the phyloFlash documentation:
https://github.com/HRGV/phyloFlash/wiki

Note: Make sure to set the path to the downloaded database when running phyloFlash.
"

## Clean up
rm 138.1.tar.gz

## Deactivate conda environment
conda deactivate

echo "phyloFlash installation and configuration completed successfully"
