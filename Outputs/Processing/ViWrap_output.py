import csv

def read_viwrap_output(file_path):
    viwrap_data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            viwrap_data.append(row)
    return viwrap_data

def read_viral_gcf_mapping(file_path):
    gcf_mapping = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gcf_id = row['GCF_ID'].strip()
            sequence_ids = row['Sequence_IDs'].strip().split(';')
            for seq_id in sequence_ids:
                gcf_mapping[seq_id] = gcf_id
    return gcf_mapping

def create_viwrap_output(viwrap_data, gcf_mapping):
    output_data = []

    for entry in viwrap_data:
        nc_id = entry['seq_name']
        taxonomy = entry['taxonomy']

        gcf_id = gcf_mapping.get(nc_id)

        if gcf_id:
            taxonomy_levels = taxonomy.split(';')
            kingdom = taxonomy_levels[0] if len(taxonomy_levels) > 0 else ''
            outra_tax_1 = taxonomy_levels[1] if len(taxonomy_levels) > 1 else ''
            outra_tax_2 = taxonomy_levels[2] if len(taxonomy_levels) > 2 else ''
            phylum = taxonomy_levels[3] if len(taxonomy_levels) > 3 else ''
            class_ = taxonomy_levels[4] if len(taxonomy_levels) > 4 else ''
            order = taxonomy_levels[5] if len(taxonomy_levels) > 5 else ''
            family = taxonomy_levels[6] if len(taxonomy_levels) > 6 else ''
            genus = taxonomy_levels[7] if len(taxonomy_levels) > 7 else ''
            species = taxonomy_levels[8] if len(taxonomy_levels) > 8 else ''

            output_data.append([
                nc_id,
                gcf_id,
                gcf_id,
                kingdom,
                outra_tax_1,
                outra_tax_2,
                phylum,
                class_,
                order,
                family,
                genus,
                species
            ])
    
    return output_data

def save_viwrap_output(output_data, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Original_ID', 'GCF_ID', 'index', 'Kingdom', 'Outra Tax 1', 'Outra Tax 2', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'])
        
        for row in output_data:
            writer.writerow(row)

def main():
    viwrap_file_path = input("Enter the path to the ViWrap output file (e.g., combined_viralgenomes_virus_summary.tsv): ")
    viral_gcf_mapping_file_path = input("Enter the path to the viral GCF mapping file (e.g., viral_gcf_sequence_id_mapping.csv): ")
    output_file_path = input("Enter the path to save the ViWrap output CSV file (e.g., viwrap_output.csv): ")

    viwrap_data = read_viwrap_output(viwrap_file_path)
    gcf_mapping = read_viral_gcf_mapping(viral_gcf_mapping_file_path)

    output_data = create_viwrap_output(viwrap_data, gcf_mapping)
    
    save_viwrap_output(output_data, output_file_path)

    print(f"ViWrap output saved to: {output_file_path}")

if __name__ == "__main__":
    main()
