import csv
from collections import defaultdict

def read_phabox_results(file_path):
    results = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            if len(row) >= 3 and row[2] != "filtered" and row[2] != "unpredicted":
                accession, lineage = row[0], row[2]
                taxonomy = parse_lineage(lineage)
                results[accession] = taxonomy
    return results

def parse_lineage(lineage):
    taxonomy = {
        'Kingdom': '', 'Phylum': '', 'Class': '', 'Family': '', 'Genus': ''
    }
    parts = lineage.split(';')
    for part in parts:
        if ':' in part:
            level, name = part.split(':', 1)
            if level == 'superkingdom':
                taxonomy['Kingdom'] = name
            elif level.lower() in ['phylum', 'class', 'family', 'genus']:
                taxonomy[level.capitalize()] = name
        else:
            print(f"Warning: Skipping malformed lineage part '{part}'")
    return taxonomy

def read_id_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            mapping[row['New_ID']] = row['Original_ID']
    return mapping

def read_gcf_to_nc_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            gcf_id = row[0]
            nc_ids = row[1].split(';')
            mapping[gcf_id] = nc_ids[0]
    return mapping

def read_true_taxonomy(file_path, gcf_to_nc_mapping):
    taxonomy = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gcf_id = row['assembly_accession']
            if gcf_id in gcf_to_nc_mapping:
                nc_id = gcf_to_nc_mapping[gcf_id]
                taxonomy[nc_id] = {
                    'Kingdom': row['Kingdom'],
                    'Phylum': row['Phylum'],
                    'Class': row['Class'],
                    'Family': row['Family'],
                    'Genus': row['Genus'],
                    'GCF_ID': gcf_id
                }
    return taxonomy

def write_combined_results(phabox_results, id_mapping, true_taxonomy, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['NC_ID', 'GCF_ID', 'Kingdom', 'Phylum', 'Class', 'Family', 'Genus'])
        
        for new_id, original_id in id_mapping.items():
            if new_id in phabox_results and original_id in true_taxonomy:
                phabox_taxonomy = phabox_results[new_id]
                nc_id = true_taxonomy[original_id]['GCF_ID']
                writer.writerow([
                    original_id,
                    nc_id,
                    phabox_taxonomy['Kingdom'],
                    phabox_taxonomy['Phylum'],
                    phabox_taxonomy['Class'],
                    phabox_taxonomy['Family'],
                    phabox_taxonomy['Genus']
                ])

def main():
    phabox_file = input("Enter the path to the PhaBOX output file (e.g., phagcn_prediction.tsv): ")
    id_mapping_file = input("Enter the path to the ID mapping file (e.g., id_mapping_phabox.tsv): ")
    true_taxonomy_file = input("Enter the path to the true taxonomy file (e.g., viral_taxonomy_mapping.csv): ")
    gcf_to_nc_mapping_file = input("Enter the path to the GCF to NC mapping file (e.g., viral_gcf_sequence_id_mapping.csv): ")
    output_file = input("Enter the path to save the combined output CSV file: ")

    phabox_results = read_phabox_results(phabox_file)
    id_mapping = read_id_mapping(id_mapping_file)
    gcf_to_nc_mapping = read_gcf_to_nc_mapping(gcf_to_nc_mapping_file)
    true_taxonomy = read_true_taxonomy(true_taxonomy_file, gcf_to_nc_mapping)
    
    write_combined_results(phabox_results, id_mapping, true_taxonomy, output_file)
    
    print(f"Formatted PhaBOX results have been written to {output_file}")

if __name__ == "__main__":
    main()
