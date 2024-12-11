#!/bin/bash

# TAR-VIR Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone TAR-VIR repository
git clone --recursive https://github.com/chjiao/TAR-VIR.git
cd TAR-VIR

## Build Overlap_extension
cd Overlap_extension
make
cd ..

## Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential

## Install Overlap_extension using conda
conda install -c kennethshang overlap_extension -y

## Test the installation
cd Overlap_extension
./build -f test_data/virus.fa -o virus
./overlap -S test_data/HIV.sam -x virus -f test_data/virus.fa -c 180 -o virus_recruit.fa

## Provide usage instructions
echo "
TAR-VIR installation completed successfully.

For more information and specific usage instructions, refer to the TAR-VIR documentation:
https://github.com/chjiao/TAR-VIR
"

echo "TAR-VIR installation and configuration completed successfully"


