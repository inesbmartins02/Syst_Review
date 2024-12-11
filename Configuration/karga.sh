#!/bin/bash

# KARGA Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone KARGA repository
git clone https://github.com/DataIntellSystLab/KARGA.git
cd KARGA

## Create and activate conda environment
conda create -n karga_env python=3.8 -y
conda activate karga_env

## Install KARGA dependencies
pip install -r requirements.txt

## Install KARGA
pip install .

## Verify installation
echo "Verifying KARGA installation..."
python -c "import karga; print(karga.__version__)"

## Provide usage instructions
echo "
KARGA installation completed successfully.

To use KARGA:

1. Activate the conda environment:
   conda activate karga_env

2. Run KARGA:
   python -m karga [options]

For more information and specific usage instructions, refer to the KARGA documentation in the GitHub repository.
"

## Deactivate conda environment
conda deactivate

echo "KARGA installation and configuration completed successfully"

