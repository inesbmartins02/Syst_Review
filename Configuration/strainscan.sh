#!/bin/bash

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone StrainScan repository
git clone https://github.com/liaoherui/StrainScan.git
cd StrainScan

## Clone SibeliaZ repository
git clone https://github.com/medvedevgroup/SibeliaZ
cd SibeliaZ

## Create build directory and compile SibeliaZ
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make
sudo make install
cd ../../

## Verify SibeliaZ installation
sibeliaz --version

## Create and activate conda environment for StrainScan
conda create -n strainscan python=3.7 -y
conda activate strainscan

## Install dependencies for StrainScan
conda install numpy=1.17.3 pandas=1.0.1 biopython=1.74 scipy=1.3.1 scikit-learn=0.23.1 -y

## Compile SibeliaZ within the conda environment
cd SibeliaZ
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
make install
cd ../../

## Change permissions for executable files in StrainScan
cd StrainScan
chmod 755 library/jellyfish-linux
chmod 755 library/dashing_s128

## Install treelib using pip
pip install treelib

## Verify StrainScan installation
python StrainScan.py -h

## Download pre-built databases (optional)
echo "Do you want to download the pre-built databases? (yes/no)"
read -r download_db
if [ "$download_db" = "yes" ]; then
    cd Download_DB_script
    sh ecoli_db.sh
    cd ..
fi

## Deactivate conda environment
conda deactivate

echo "StrainScan and SibeliaZ installation and configuration completed successfully"
