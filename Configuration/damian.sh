#!/bin/bash

# Tool Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Check versions of required software
echo "Checking required software versions..."
ruby --version
perl --version
java -version

## Install dependencies
echo "Installing dependencies..."
sudo yum install ruby-devel postgresql-devel perl-core perl-JSON perl-Digest-MD5 wget unzip -y

## Install required gems
echo "Installing required Ruby gems..."
gem install pg -v 0.19
gem install nokogiri -v 1.6.8.1
gem install axlsx
gem install amatch

## Download and install Trimmomatic
echo "Downloading and installing Trimmomatic..."
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
unzip Trimmomatic-0.39.zip
mv Trimmomatic-0.39 /usr/local/
echo 'export PATH=$PATH:/usr/local/Trimmomatic-0.39' >> ~/.bashrc

## Download and install Bowtie2
echo "Downloading and installing Bowtie2..."
wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.5/bowtie2-2.4.5-linux-x86_64.zip
unzip bowtie2-2.4.5-linux-x86_64.zip
mv bowtie2-2.4.5-linux-x86_64 /usr/local/
echo 'export PATH=$PATH:/usr/local/bowtie2-2.4.5-linux-x86_64' >> ~/.bashrc

## Download and install HMMER
echo "Downloading and installing HMMER..."
wget http://eddylab.org/software/hmmer/hmmer.tar.gz
tar zxf hmmer.tar.gz
cd hmmer-3.3.2
./configure
make
sudo make install
cd ..

## Download and install BLAST+
echo "Downloading and installing BLAST+..."
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz
tar zxf ncbi-blast-2.13.0+-x64-linux.tar.gz
mv ncbi-blast-2.13.0+ /usr/local/
echo 'export PATH=$PATH:/usr/local/ncbi-blast-2.13.0+/bin' >> ~/.bashrc

## Download and install IDBA_UD
echo "Downloading and installing IDBA_UD..."
git clone https://github.com/loneknightpy/idba.git
cd idba
./build.sh
sudo make install
cd ..

## Download third-party dependencies
echo "Downloading third-party dependencies..."
sh 3rd_party/download_dependencies.sh

## Download databases
echo "Downloading databases..."
sh databases/get_all.sh

## Populate DAMIAN's internal database
echo "Populating DAMIAN's internal database..."
ruby damian_database.rb  --erase_and_rebuild --names databases/tax/names.dmp --nodes databases/tax/nodes.dmp --hmm databases/pfam/Pfam-A.hmm.txt --taxdepth databases/pfam/pfamA_tax_depth.txt

## Verify installation
echo "Verifying installation..."
trimmomatic -version
bowtie2 --version
hmmsearch -h
blastn -version
idba_ud --help

echo "Installation and configuration completed successfully"

# Source the updated .bashrc to make the new PATH additions available
source ~/.bashrc




