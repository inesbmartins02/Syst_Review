#!/bin/bash

# TaxIt Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone TaxIt repository
git clone --recursive --depth=1 https://gitlab.com/mkuhring/TaxIt.git
cd TaxIt

## Create and activate conda environment
conda create --name taxit -y
source activate taxit

## Install required packages
conda install -c defaults --override-channels openjdk=8.0 maven=3.5.3 perl=5 r-ggplot2=2.2.1 rpy2=2 bioconda::snakemake=3.13.3 bioconda::msgf_plus=2016.10.26 bioconda::xtandem=15.12.15.2 bioconda::seqkit=0.7.0 -y

## Build Java modules
cd modules_java
mvn clean package
cd ..

## Download reference databases
mkdir -p databases
cd databases

# For bacteria 
wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/bacteria/*.protein.faa.gz
gzip -d bacteria.*.protein.faa.gz 
cat bacteria.*.protein.faa > refseq_bacteria.fasta
rm bacteria.*.protein.faa.gz

# For viruses 
wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/*.protein.faa.gz
gzip -d viral.*.protein.faa.gz
cat viral.*.protein.faa > refseq_viral.fasta
rm viral.*.protein.faa

# Download taxonomy files 
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
gzip -d prot.accession2taxid.gz
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz 
tar xfzv taxdump.tar.gz
rm taxdump.tar.gz

cd ..

## Provide usage instructions
echo "
TaxIt installation completed successfully.

For more information and specific usage instructions, refer to the TaxIt documentation:
https://gitlab.com/mkuhring/TaxIt
"

