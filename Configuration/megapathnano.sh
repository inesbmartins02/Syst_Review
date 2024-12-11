#!/bin/bash

# MegaPath-Nano Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $LINENO"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

echo "Starting MegaPath-Nano installation..."

# Prioritize channels
echo "Configuring conda channels..."
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

# Create and activate conda environment
echo "Creating and activating conda environment..."
conda create -n mpn python=3.6.10 -y
source activate mpn

# Install dependencies
echo "Installing dependencies..."
conda install -y pandas psutil pybedtools porechop==0.2.4 bioconvert seqtk minimap2 bcftools samtools==1.9 'pysam>=0.16.0' tabulate cgecore==1.5.6 "ncbi-amrfinderplus>=3" "rgi>=5"
conda install -y mamba
mamba install -y clair=2.1.1 parallel=20191122

# Clone MegaPath-Nano
echo "Cloning MegaPath-Nano repository..."
git clone --depth 1 https://github.com/HKU-BAL/MegaPath-Nano

# Compile MegaPath-Nano-Amplicon filter module
echo "Compiling MegaPath-Nano-Amplicon filter module..."
cd MegaPath-Nano/bin/realignment/realign/
g++ -std=c++14 -O1 -shared -fPIC -o realigner ssw_cpp.cpp ssw.c realigner.cpp
g++ -std=c++11 -shared -fPIC -o debruijn_graph -O3 debruijn_graph.cpp
gcc -Wall -O3 -pipe -fPIC -shared -rdynamic -o libssw.so ssw.c ssw.h
cd -

cd MegaPath-Nano/bin/Clair-ensemble/Clair.beta.ensemble.cpu/clair/
g++ ensemble.cpp -o ensemble
cd -

cd MegaPath-Nano/bin/samtools-1.13
./configure && make && make install
cd -

echo "Downloading and extracting Taxon database..."
wget -c http://www.bio8.cs.hku.hk/dataset/MegaPath-Nano/MegaPath-Nano_db.v1.0.tar.gz -O - | tar -xvz

# Setup AMR databases 
echo "Setting up AMR databases..."
rgi load --card_json MegaPath-Nano/bin/amr_db/card/card.json
amrfinder -u

# Download and extract Amplicon filter module database 
echo "Downloading and extracting Amplicon filter module database..."
wget -c http://www.bio8.cs.hku.hk/dataset/MegaPath-Nano/MegaPath-Nano-Amplicon_db.v1.0.tar.gz -O - | tar -xvz

# Deactivate conda environment
conda deactivate

echo "MegaPath-Nano installation and configuration completed successfully!"



