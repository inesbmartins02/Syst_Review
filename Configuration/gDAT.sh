#!/bin/bash

# gDAT Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone gDAT repository
git clone https://github.com/ut-planteco/gDAT.git
cd gDAT

## Create and activate conda environment
conda create --name gdat_env python=3 -y
conda activate gdat_env

## Install required packages
conda install -y vsearch
conda install -y -c bioconda blast
conda install -y -c bioconda flash
conda install -y python-tk

## Install display dependencies
sudo apt-get update
sudo apt-get install -y xorg xvfb

## Set up virtual display
echo "Setting up virtual display..."
Xvfb :99 &
export DISPLAY=:99

## Verify installation
echo "Verifying installation..."
vsearch --version
blastn -version
flash --version
python -c "import tkinter; print('Tkinter is installed')"

## Provide usage instructions
echo "gDAT installation completed successfully.

Note: If you encounter display issues, ensure that Xvfb is running:
Xvfb :99 &
export DISPLAY=:99

For more information, refer to the gDAT documentation.
"
## Deactivate conda environment
conda deactivate


