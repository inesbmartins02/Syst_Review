import csv

def main():
    tama_output_file = input("Enter the path to the TAMA output file (e.g., tama_output.csv): ")
    taxonomy_mapping_file = input("Enter the path to the taxonomy mapping file (e.g., bacteria_taxonomy_mapping.csv): ")

    taxonomy_mapping = {}
    with open(taxonomy_mapping_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assembly_accession = row['assembly_accession']
            species_taxid = row['species_taxid']
            taxonomy_mapping[assembly_accession] = species_taxid

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    with open(tama_output_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        for gcf_id, taxon_ids in reader:
            taxon_ids_list = taxon_ids.replace('"', '').split(',')
            
            if gcf_id in taxonomy_mapping:
                correct_species_taxid = taxonomy_mapping[gcf_id]
                
                if correct_species_taxid in taxon_ids_list:
                    true_positives += 1
                else:
                    false_negatives += 1  
            else:
                false_positives += 1  

    total_gcf_ids = len(taxonomy_mapping)  
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print(f"Total de classificações: {total_gcf_ids}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1_score:.2f}")

if __name__ == "__main__":
    main()
