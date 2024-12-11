#!/bin/bash

# Exit on error
set -e

# Create and activate ViWrap environment
conda create -c bioconda -c conda-forge -n ViWrap python=3.8 biopython=1.80 mamba=1.3.0 numpy=1.24.2 pandas=1.5.3 pyfastx=0.8.4 matplotlib=3.6.3 seaborn=0.12.2 diamond=2.0.15 hmmer=3.3.2 -y
source activate ViWrap

# Clone ViWrap repository
git clone https://github.com/AnantharamanLab/ViWrap
cd ViWrap

# Make scripts executable and add to PATH
chmod +x ViWrap scripts/*.py
export PATH=$(pwd):$PATH

# Set up ViWrap conda environments
CONDA_ENV_DIR="/mnt/storagelv/home/inesbrancomartins/miniforge3/envs"
ViWrap set_up_env --conda_env_dir $CONDA_ENV_DIR

# Download ViWrap databases
DB_DIR="/path/to/ViWrap_db"
ViWrap download --db_dir $DB_DIR --conda_env_dir $CONDA_ENV_DIR

# Create and activate geNomad environment
conda create -n ViWrap-geNomad -c bioconda genomad -y
conda activate ViWrap-geNomad

# Download geNomad database
GENOMAD_DB_DIR="${DB_DIR}/genomad_db"
mkdir -p $GENOMAD_DB_DIR
genomad download-database $GENOMAD_DB_DIR

# Verify installation
ViWrap -h
ViWrap run -h
genomad --version

echo "ViWrap and geNomad installation and configuration completed."

