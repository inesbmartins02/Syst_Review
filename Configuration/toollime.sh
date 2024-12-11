#!/bin/bash

# LiME Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone LiME repository
git clone https://github.com/veronicaguerrini/LiME.git
cd LiME

## Compile LiME with default settings
echo "Compiling LiME with default settings (ebwt=1)..."
make

## Compile LiME with ebwt=0
echo "Compiling LiME with ebwt=0..."
make EBWT=0

## Compile LiME with HIGHER=1
echo "Compiling LiME with HIGHER=1..."
make HIGHER=1

## Make the installation script executable and run it
chmod +x Install_tools_preprocessing.sh
./Install_tools_preprocessing.sh

## Provide usage instructions
echo "
LiME installation completed successfully.

For more information and specific usage instructions, refer to the LiME documentation:
https://github.com/veronicaguerrini/LiME
"


