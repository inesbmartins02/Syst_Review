#!/bin/bash

# BAGEP Installation and Configuration Script
# This script installs and configures BAGEP (Bacterial Genome Pipeline)

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone BAGEP repository
git clone https://github.com/idolawoye/BAGEP.git
cd BAGEP

## Create and activate conda environment
conda env create -f environment.yml
conda activate bagep

## Install Centrifuge
wget -c ftp://ftp.ccb.jhu.edu/pub/infphilo/centrifuge/data/p_compressed+h+v.tar.gz
mkdir -p $HOME/centrifuge-db
tar -C $HOME/centrifuge-db -zxvf p_compressed+h+v.tar.gz
echo "export CENTRIFUGE_DEFAULT_DB=$HOME/centrifuge-db/p_compressed+h+v" >> ~/.bashrc
source ~/.bashrc

## Configure Krona Taxonomy Plot
rm -rf ~/miniconda3/envs/bagep/opt/krona/taxonomy
mkdir -p ~/krona/taxonomy
ln -s ~/krona/taxonomy/ ~/miniconda3/envs/bagep/opt/krona/taxonomy
ktUpdateTaxonomy.sh ~/krona/taxonomy

## Create directory for fastq files
mkdir fastq

## Verify installations
echo "Verifying installations..."
conda list | grep bagep
centrifuge --version
ktUpdateTaxonomy.sh --version

## Cleanup
rm p_compressed+h+v.tar.gz

## Deactivate conda environment
conda deactivate

echo "BAGEP installation and configuration completed successfully"
