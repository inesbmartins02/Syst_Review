#!/bin/bash

# FacePAI Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $LINENO: $BASH_COMMAND"
    exit 1
}

# Set up error handling
trap 'handle_error' ERR

## Clone FacePAI repository
git clone https://github.com/emmawahl/facepai.git
cd facepai

## Make scripts executable
chmod u+x *.sh

## Create and activate conda environment
conda create -n facepai python=3.7 -y
conda activate facepai

## Configure conda channels
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

## Install required packages
conda install -y fastp vsearch cutadapt swarm blast seqtk

## Prepare BOLD database
gunzip BOLD_Public.18-Oct-2024.fasta.gz
./caprese.sh -P BOLD BOLD_Public.18-Oct-2024.fasta
makeblastdb -in BOLD_prepared.fasta -title "BOLD_database" -dbtype nucl

## Configure options.config
echo 'BLASTDB="BOLD_prepared.fasta"' > options.config

## Verify installation
echo "Verifying installation..."
fastp --version
vsearch --version
cutadapt --version
swarm --version
blastn -version
seqtk 2>&1 | head -n 1

## Provide usage instructions
echo "FacePAI installation completed successfully"
echo "To use FacePAI, activate the conda environment with: conda activate facepai"

## Deactivate conda environment
conda deactivate