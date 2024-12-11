#!/bin/bash

# GPA Package Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone GPA repository
git clone https://github.com/IID-DTH/GPA-package.git
cd GPA-package

## Create and activate conda environment
conda create -n gpa_env python=3.8 -y
conda activate gpa_env

## Install dependencies
conda install -c bioconda samtools bedtools gatk4 picard bwa -y

## Download and install ANNOVAR
wget http://www.openbioinformatics.org/annovar/download/0wgxR2rIVP/annovar.latest.tar.gz
tar -zxvf annovar.latest.tar.gz

## Add ANNOVAR to PATH
echo 'export PATH="$PWD/annovar:$PATH"' >> ~/.bashrc
source ~/.bashrc

## Verify installation
echo "Verifying installation..."
samtools --version
bedtools --version
gatk --version
picard ViewSam --version
bwa
annotate_variation.pl

## Provide usage instructions
echo "GPA package installation completed successfully."

## Deactivate conda environment
conda deactivate

## Clean up
rm annovar.latest.tar.gz





