#!/bin/bash

# DCiPatho Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone DCiPatho repository
git clone https://github.com/LorMeBioAI/DCiPatho.git
cd DCiPatho

## Create and activate conda environment
conda create -n dcipatho python=3.7 -y
conda activate dcipatho

## Install dependencies
conda install numpy=1.19.5 pandas=1.1.5 scikit-learn=0.24.2 -y
conda install matplotlib -y
conda install pytorch=1.10.0 -c pytorch -y

## Verify installation
python -c "import numpy, torch, pandas, sklearn; print('Installation successful!')"

## Download additional files
# Note: Replace with actual paths or prompt user for paths
echo "Please provide the path to the NCBI_download.py file:"
read -r ncbi_download_path
scp "$ncbi_download_path" .

echo "Please provide the path to the NCBI_22June_RefSeq_32927_Complete_1NP_2P_taxnonmy.csv file:"
read -r ncbi_csv_path
scp "$ncbi_csv_path" .

echo "Please provide the path to the DCiPatho_best_k3-7_model.pt file:"
read -r model_path
scp "$model_path" .

## Configure DCiPatho
# Prompt user for paths
echo "Please provide the path to your input FASTA files:"
read -r fasta_path

echo "Please provide the path to save the prediction results:"
read -r save_res_path

# Use sed to update the configuration file
sed -i "s|self.best_model_name = .*|self.best_model_name = '$model_path'|" DCiPatho_config.py
sed -i "s|self.raw_fasta_path = .*|self.raw_fasta_path = '$fasta_path'|" DCiPatho_config.py
sed -i "s|self.save_res_path = .*|self.save_res_path = '$save_res_path'|" DCiPatho_config.py

## Deactivate conda environment
conda deactivate

echo "DCiPatho installation and configuration completed successfully"




