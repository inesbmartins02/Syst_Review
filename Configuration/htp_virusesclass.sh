#!/bin/bash

# Viruses Classifier Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

echo "Starting Viruses Classifier installation..."

# Create and activate conda environment
conda create -n viruses_classifier python=2.7 -y
source activate viruses_classifier

# Install dependencies
echo "Installing dependencies..."
conda install numpy=1.13.3 scipy=0.13.3 scikit-learn=0.19.2 -y

# Clone viruses_classifier repository
echo "Cloning viruses_classifier repository..."
git clone https://github.com/wojciech-galan/viruses_classifier.git
cd viruses_classifier

# Verify installation
echo "Verifying installation..."
python -m viruses_classifier -h

# Deactivate conda environment
conda deactivate

echo "Installation script completed."

