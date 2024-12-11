#!/bin/bash

# TAMA Installation and Configuration Script

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

## Clone TAMA repository
git clone https://github.com/jkimlab/TAMA.git
cd TAMA

## Install system dependencies
sudo apt update
sudo apt install -y perl default-jdk git gcc g++ make zip unzip curl python

## Run TAMA setup
./setup.pl --install

## Source environment file
source ./src/env.sh

## Download the databases (this may take several hours)
echo "Downloading databases. This may take several hours..."
./setup.pl --db --species

## Create parameter file
cat > meus_parametros.txt <<EOL
[Project]
\$PROJECTNAME=MeuProjeto

[Basic_options]
\$TOOL=CLARK,centrifuge,kraken
\$RANK=species
\$META-THRESHOLD=0.34
\$WEIGHT-CLARK=0.9374
\$WEIGHT-centrifuge=0.9600
\$WEIGHT-kraken=0.9362

[Database]
\$DBNAME=meu_banco_de_dados

[Input]
>minha_amostra1
\$PAIRED1=caminho/para/amostra1_1.fastq 
\$PAIRED2=caminho/para/amostra1_2.fastq

>minha_amostra2
\$PAIRED1=caminho/para/amostra2_1.fastq
\$PAIRED2=caminho/para/amostra2_2.fastq
EOL

## Provide usage instructions
echo "
TAMA installation completed successfully.

For more information and specific usage instructions, refer to the TAMA documentation.
"


