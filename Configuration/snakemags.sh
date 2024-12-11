#!/bin/bash

# SnakeMAGs Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone SnakeMAGs repository
git clone https://github.com/Nachida08/SnakeMAGs.git
cd SnakeMAGs

## Install mamba if not already installed
conda install -n base -c conda-forge mamba -y

## Create and activate snakemake environment
conda activate base
mamba create -c conda-forge -c bioconda -n snakemake snakemake -y
conda activate snakemake

## Download GTDB database
wget https://data.gtdb.ecogenomic.org/releases/latest/auxillary_files/gtdbtk_package/full_package/gtdbtk_data.tar.gz
tar -xzvf gtdbtk_data.tar.gz
rm gtdbtk_data.tar.gz

## Configure config.yaml
# Note: Replace the placeholders with actual paths
cat > config.yaml <<EOL
working_dir: "/path/to/your/working/directory/"
raw_fastq: "/path/to/your/fastq/files/"
suffix_1: "_R1.fastq"
suffix_2: "_R2.fastq"
conda_env: "/path/to/SnakeMAGs_conda_env/"
adapters: "/path/to/adapters.fa"
GTDB_data_ref: "$PWD/release207_v2"
gunc: "no"
EOL

echo "Please edit config.yaml with your specific paths and settings."

## Provide usage instructions
echo "
SnakeMAGs installation completed successfully.

For more information and specific usage instructions, refer to the SnakeMAGs documentation:
https://github.com/Nachida08/SnakeMAGs
"

echo "SnakeMAGs installation and configuration completed successfully"





