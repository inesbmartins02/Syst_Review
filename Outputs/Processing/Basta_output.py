import csv

def normalize_name(name):
    """Replaces underscores with spaces and maintains capitalization."""
    return name.replace("_", " ") if name else ""

def transform_output_to_csv(input_file, gcf_mapping_file, output_file):
    gcf_mapping = {}
    with open(gcf_mapping_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')  
        next(reader)  
        for row in reader:
            if len(row) >= 2:
                gcf_id = row[0].strip()
                nc_ids = row[1].strip().split(';')
                for nc_id in nc_ids:
                    gcf_mapping[nc_id] = gcf_id 

    with open(input_file, 'r') as f:
        lines = f.readlines()

    transformed_data = []

    for line in lines:
        parts = line.strip().split('\t')  
        if len(parts) < 1:
            continue  

        nc_id = parts[0] 
        lineage = parts[1] if len(parts) > 1 else "Unknown"  

        lineage_parts = lineage.split(';')
        
        kingdom = lineage_parts[0] if len(lineage_parts) > 0 else ""
        phylum = lineage_parts[1] if len(lineage_parts) > 1 else ""
        class_tax = lineage_parts[2] if len(lineage_parts) > 2 else ""
        order = lineage_parts[3] if len(lineage_parts) > 3 else ""
        family = lineage_parts[4] if len(lineage_parts) > 4 else ""
        genus = lineage_parts[5] if len(lineage_parts) > 5 else ""
        species = lineage_parts[6] if len(lineage_parts) > 6 else ""

        genus_normalized = normalize_name(genus)
        species_normalized = normalize_name(species)

        gcf_id = gcf_mapping.get(nc_id, "")  

        transformed_data.append([nc_id, gcf_id, kingdom, phylum, class_tax, order, family, genus_normalized, species_normalized])

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NC_ID', 'GCF_ID', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'])
        
        writer.writerows(transformed_data)

def main():
    input_file_path = input("Enter the path to the Basta output file: ")
    gcf_mapping_file_path = input("Enter the path to the GCF mapping file for the tested domain: ")
    output_file_path = input("Enter the path to save the output CSV file: ")

    transform_output_to_csv(input_file_path, gcf_mapping_file_path, output_file_path)

    print(f"Data transformed and saved in {output_file_path}")

if __name__ == "__main__":
    main()
