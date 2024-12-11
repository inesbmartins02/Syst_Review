#!/bin/bash

# VIGA Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone VIGA repository
git clone https://github.com/viralInformatics/VIGA.git
cd VIGA

## Create and activate conda environment
conda create -n viga_env python=3.6 -y
conda activate viga_env

## Install required packages
conda install -y fastp=0.12.4 trinity=2.8.5 diamond=2.0.11.149 ragtag=2.1.0 quast=5.0.2
pip install pandas==1.1.5 numpy==1.19.5 matplotlib==3.3.4 biopython==1.79

## Download databases
mkdir -p ./db

# Download and extract taxdmp.zip (FALTA A PARTIR DAQUI)
wget -P ./db https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip
unzip ./db/taxdmp.zip -d ./db

# Download prot.accession2taxid
wget -P ./db https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
gunzip ./db/prot.accession2taxid.gz

# Download and process RefSeqVirusProtein
wget -c ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.protein.faa.gz
gunzip viral.1.protein.faa.gz
mv viral.1.protein.faa RefSeqVirusProtein

# Download and extract nr database
wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz
gunzip nr.gz

# Create DIAMOND databases
diamond makedb --in RefSeqVirusProtein -d Diamond_RefSeqVirusProtein --taxonmap ./db/prot.accession2taxid --taxonnodes ./db/nodes.dmp
diamond makedb --in nr -d Diamond_nr --taxonmap ./db/prot.accession2taxid --taxonnodes ./db/nodes.dmp

## Provide usage instructions
echo "
VIGA installation and database setup completed successfully.

For more information and specific usage instructions, refer to the VIGA documentation:
https://github.com/viralInformatics/VIGA
"

