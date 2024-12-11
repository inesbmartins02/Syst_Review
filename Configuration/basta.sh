#!/bin/bash

# BASTA Installation and Configuration Script
# This script installs and configures BASTA (Basic Sequence Taxonomy Annotation)

# Exit if any command fails
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred at line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

# Clone BASTA repository
git clone https://github.com/timkahlke/BASTA.git
cd BASTA

# Install BASTA
python setup.py install

# Run basta taxonomy
basta taxonomy

# Download UniProt database and mapping files
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip uniprot_sprot.fasta.gz

wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz
gunzip idmapping_selected.tab.gz

# Create a BLAST db
makeblastdb -in uniprot_sprot.fasta -dbtype prot
blastx -query combined_sequences.fasta -db uniprot_sprot.fasta -out resultados_blast2.txt -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"


# Create BASTA mapping file
python - <<EOF
import csv
import sys

csv.field_size_limit(sys.maxsize)

def process_idmapping(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        for row in reader:
            if len(row) >= 13:
                uniprot_id = row[0]
                taxon_id = row[12]
                if taxon_id:
                    writer.writerow([uniprot_id, taxon_id])

    print(f"Mapping file '{output_file}' created successfully.")

process_idmapping('idmapping_selected.tab', 'basta_uniprot_mapping.tab')
EOF

# Create BASTA database
basta create_db basta_uniprot_mapping.tab uni_mapping.db 0 1

# Verify installation
echo "Verifying BASTA installation..."
basta --version

echo "BASTA installation and configuration completed successfully"







