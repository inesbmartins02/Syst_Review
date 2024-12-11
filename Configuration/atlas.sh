#!/bin/bash

# ATLAS Installation and Configuration Script
# This script installs and configures ATLAS (Assembly and Taxonomic Analysis of Sequencing Data)

# Clone the ATLAS repository
git clone https://github.com/metagenome-atlas/atlas.git
cd atlas
pip install .

# Create and activate conda environment
mamba env create -n atlas-dev --file atlasenv.yml
conda activate atlas-dev

# Install ATLAS
pip install --editable .

# Return to parent directory
cd ..

# Download test data
wget https://zenodo.org/record/3992790/files/test_reads.tar.gz

# Extract test data
tar -xzf test_reads.tar.gz

# Verify ATLAS installation
atlas --version

# Start a new project
atlas init --db-dir databases /mnt/storagelv/home/inesbrancomartins/Tese/database/refdb/test_reads

# Exit script if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

# Remove downloaded archive
rm test_reads.tar.gz

# Deactivate conda environment
conda deactivate

# Note: Atlas is designed to automatically install the necessary databases at runtime (You need to specify a directory to store these databases using the --db-dir option when initializing the project) -> Installation process: When you run Atlas for the first time, it will automatically download and install the necessary databases, including GTDB.

echo "ATLAS installation and configuration completed successfully"


