#!/bin/bash

# ARGem Installation and Configuration Script
# ARGem is a comprehensive metagenomics pipeline specifically designed for analyzing antibiotic resistance genes (ARGs) in environmental samples. 
# This script installs and configures all necessary tools for ARGem

### Environment Setup
# Clone the repository
git clone https://github.com/xlxlxlx/ARGem.git

# Create and activate conda environment
conda create --name argem python=3.9
conda activate argem

# Install required Python packages
pip install -r requirements_w_versions.txt

### Tool Installation

# 1. SRA Toolkit
# Install SRA Toolkit dependencies
sudo apt update
sudo apt install libncurses5 libbz2-dev liblzma-dev libcurl4-openssl-dev -y
# Download and install SRA Toolkit
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-ubuntu64.tar.gz
tar -zxvf sratoolkit.current-ubuntu64.tar.gz
mkdir -p /mnt/storagelv/home/inesbrancomartins/Tese/tools/ARGem/sratoolkit
sudo mv sratoolkit.* /mnt/storagelv/home/inesbrancomartins/Tese/tools/ARGem/sratoolkit
# Add SRA Toolkit to PATH
echo 'export PATH=$PATH:/mnt/storagelv/home/inesbrancomartins/Tese/tools/ARGem/sratoolkit/bin' >> ~/.bashrc
source ~/.bashrc

# 2. Python
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip -y
# Verify installation
python3 --version
pip3 --version

# 3. MySQL
# Install MySQL
sudo apt update
sudo apt install mysql-server -y
sudo mysql_secure_installation
# Verify installation
mysql --version

# 4. Diamond
# Download and install DIAMOND
wget https://github.com/bbuchfink/diamond/releases/download/v0.9.32/diamond-linux64.tar.gz
tar xzf diamond-linux64.tar.gz
sudo mv diamond /usr/local/bin
# Verify installation
diamond --version

# 5. NCBI BLAST+
# Download and install NCBI BLAST+
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/ncbi-blast-2.9.0+-x64-linux.tar.gz
tar -zxvf ncbi-blast-2.9.0+-x64-linux.tar.gz
sudo mv ncbi-blast-2.9.0+ /usr/local/ncbi-blast
# Add NCBI BLAST+ to PATH
echo 'export PATH=$PATH:/usr/local/ncbi-blast/bin' >> ~/.bashrc
source ~/.bashrc
# Verify installation
blastn -version

# Download the reference database - MobileGeneticElementDatabase
git clone https://github.com/KatariinaParnanen/MobileGeneticElementDatabase.git
cd MobileGeneticElementDatabase
tar -xzvf MGEs_FINAL_99perc_trim.fasta.tar.gz
# Process de database with diamond
diamond makedb --in MGEs_FINAL_99perc_trim.fasta -d MGEs_FINAL_99perc_trim
mv MGEs_FINAL_99perc_trim.dmnd driver_annotation/databases/

# Deactivate conda environment
conda deactivate
# Optional: Remove downloaded archives
rm *.tar.gz

set -e
# Your script content here
# If the script reaches this point, all commands were successful
echo "Installation completed successfully"