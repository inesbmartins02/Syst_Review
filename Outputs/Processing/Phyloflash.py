import csv
import sys

csv.field_size_limit(sys.maxsize)

def create_nz_classification_dict(sam_file):
    nz_classification = {}
    with open(sam_file, 'r') as file:
        for line in file:
            if not line.startswith('@'):
                fields = line.strip().split('\t')
                nz_id = fields[0].split(':')[0]
                classification = fields[2]
                nz_classification[nz_id] = classification
    return nz_classification

def map_nz_to_gcf(nz_classification, gcf_mapping_file):
    gcf_mapping = {}
    with open(gcf_mapping_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            gcf_id = row['GCF_ID']
            sequence_ids = row['Sequence_IDs'].split(';')
            for seq_id in sequence_ids:
                gcf_mapping[seq_id] = gcf_id

    output_file_path = input("Enter the path to save the output CSV file (e.g., output1_phyloflash.csv): ")
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NZ_ID', 'GCF_ID', 'Classification'])
        
        for nz_id, classification in nz_classification.items():
            gcf_id = gcf_mapping.get(nz_id)
            if gcf_id:
                taxonomy_parts = classification.split(' ', 1)
                if len(taxonomy_parts) > 1:
                    taxonomy_only = taxonomy_parts[1]
                else:
                    taxonomy_only = taxonomy_parts[0]
                
                writer.writerow([nz_id, gcf_id, taxonomy_only])

def expand_taxonomy_columns(input_file_path, output_file_path):
    nz_gcf_classification = []
    with open(input_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nz_id = row['NZ_ID']
            gcf_id = row['GCF_ID']
            classification = row['Classification'].split(';')
            
            while len(classification) < 7:
                classification.append('')

            new_row = {
                'NZ_ID': nz_id,
                'GCF_ID': gcf_id,
                'Kingdom': classification[0],
                'Phylum': classification[1],
                'Class': classification[2],
                'Order': classification[3],
                'Family': classification[4],
                'Genus': classification[5],
                'Species': classification[6]
            }
            nz_gcf_classification.append(new_row)

    with open(output_file_path, 'w', newline='') as file:
        fieldnames = ['NZ_ID', 'GCF_ID', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in nz_gcf_classification:
            writer.writerow(row)

def main():
    sam_file_path = input("Enter the path to the SAM file (e.g., SEQTESTE.all_archaea_16S_fragmented_250.fa.SSU.sam): ")
    gcf_mapping_file_path = input("Enter the path to the GCF mapping file (e.g., archaea_gcf_sequence_id_mapping.csv): ")
    
    nz_classification_dict = create_nz_classification_dict(sam_file_path)
    map_nz_to_gcf(nz_classification_dict, gcf_mapping_file_path)

    input_csv_path = input("Enter the path to the input CSV file (e.g., output1_phyloflash.csv): ")
    output_csv_path = input("Enter the path to save the expanded taxonomy CSV file (e.g., output_phyloflash.csv): ")
    
    expand_taxonomy_columns(input_csv_path, output_csv_path)

    print("New CSV file with taxonomic columns created successfully.")

if __name__ == "__main__":
    main()
