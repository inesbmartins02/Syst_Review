#!/bin/bash

# GPMeta Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone GPMeta repository
git clone https://github.com/Bgi-LUSH/GPMeta.git
cd GPMeta

## Install dependencies (assuming you're using a Debian-based system)
sudo apt-get update
sudo apt-get install -y build-essential cmake cuda-toolkit

## Build GPMeta
mkdir build
cd build
cmake ..
make

## Add GPMeta to PATH
echo 'export PATH="$PWD:$PATH"' >> ~/.bashrc
source ~/.bashrc

## Create directories for databases
mkdir -p databases/host
mkdir -p databases/pathogen

## Download and prepare databases - nao fiz
# Note: Replace these placeholder commands with actual database download commands
echo "Downloading host database..."
# wget -O databases/host/human.fasta [URL_TO_HOST_DATABASE]
echo "Downloading pathogen database..."
# wget -O databases/pathogen/pmseq.fasta [URL_TO_PATHOGEN_DATABASE]

## Index databases
echo "Indexing host database..."
GPMetaIndex databases/host/human.fasta index_step 0
echo "Indexing pathogen database..."
GPMetaIndex databases/pathogen/pmseq.fasta index_step 1

## Create configuration files
echo "databases/pathogen/pmseq.fasta" > ref.conf
echo "databases/pathogen/pmseq.fasta.index" > index.conf

## Provide usage instructions
echo "
GPMeta installation completed successfully.
"



