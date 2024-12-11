#!/bin/bash

# Conda and Mamba Installation Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Download Anaconda installer
wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh

## Install Anaconda
chmod +x Anaconda3-2023.07-1-Linux-x86_64.sh
bash Anaconda3-2023.07-1-Linux-x86_64.sh -b -p $HOME/anaconda3

## Add Anaconda to PATH
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

## Verify Conda installation
conda --version

## Update Conda
conda update -n base -c defaults conda -y

## Install Mamba
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o Miniforge3-Linux-x86_64.sh
chmod +x Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3

## Add Mamba to PATH
echo 'export PATH="$HOME/miniforge3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

## Verify Mamba installation
mamba --version

## Clean up installation files
rm Anaconda3-2023.07-1-Linux-x86_64.sh Miniforge3-Linux-x86_64.sh

echo "Conda and Mamba installation completed successfully"







