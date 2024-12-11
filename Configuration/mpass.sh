#!/bin/bash

# MPASS Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone MPASS repository
git clone https://github.com/s0sat/MPASS.git
cd MPASS

## Create and activate conda environment
conda create -n mpass_env python=3.8 -y
conda activate mpass_env

## Install dependencies
conda install -c bioconda perl-file-which seqtk spades blast-legacy phylip trimmomatic -y

## Download and install MetaGeneMark
# Note: You need to manually download MetaGeneMark from https://genemark.bme.gatech.edu/GeneMark/license_download.cgi
echo "Please download MetaGeneMark manually from https://genemark.bme.gatech.edu/GeneMark/license_download.cgi"
echo "After downloading, place the file in the current directory and press Enter to continue"
read -p "Press Enter to continue..."

# Assuming the downloaded file is named 'MetaGeneMark.tar.gz'
tar -xvf MetaGeneMark.tar.gz
# You may need to adjust the following line based on the extracted directory name
mv MetaGeneMark* /usr/local/bin/MetaGeneMark
echo 'export PATH=$PATH:/usr/local/bin/MetaGeneMark' >> ~/.bashrc

## Download and install BIONJ
# Note: You need to manually download BIONJ from http://www.atgc-montpellier.fr/bionj/download.php
echo "Please download BIONJ manually from http://www.atgc-montpellier.fr/bionj/download.php"
echo "After downloading, place the file in the current directory and press Enter to continue"
read -p "Press Enter to continue..."

# Assuming the downloaded file is named 'BIONJ.tar'
tar -xvf BIONJ.tar
chmod +x BIONJ_linux
mv BIONJ_linux /usr/local/bin/

## Verify installation
echo "Verifying installation..."
seqtk 2>&1 | head -n 1
spades.py --version
blastp -version
phylip -v
trimmomatic -version
MetaGeneMark -v
BIONJ_linux -h

## Provide usage instructions
echo "
MPASS installation completed successfully.

For more information and specific usage instructions, refer to the MPASS documentation.
"

## Deactivate conda environment
conda deactivate




