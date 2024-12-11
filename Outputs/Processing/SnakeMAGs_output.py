import os
import csv
import pandas as pd

def create_classification_dict(base_dir):
    results = []
    for folder in os.listdir(base_dir):
        if folder.startswith('GCF_'):
            classification_path = os.path.join(base_dir, folder, 'Classification', 'gtdbtk.ar53.summary.tsv')
            if os.path.exists(classification_path):
                df = pd.read_csv(classification_path, sep='\t')
                classification = df['classification'].iloc[0]
                parts = folder.split('_')
                if len(parts) >= 3:
                    folder_name = f"{parts[0]}_{parts[1]}.{parts[2]}"
                else:
                    folder_name = folder
                results.append([folder_name, classification])
    return results

def split_classification(classification):
    parts = classification.split(';')
    kingdom = parts[0].replace('d__', '') if parts[0].startswith('d__') else ''
    phylum = parts[1].replace('p__', '') if len(parts) > 1 and parts[1].startswith('p__') else ''
    class_ = parts[2].replace('c__', '') if len(parts) > 2 and parts[2].startswith('c__') else ''
    order = parts[3].replace('o__', '') if len(parts) > 3 and parts[3].startswith('o__') else ''
    family = parts[4].replace('f__', '') if len(parts) > 4 and parts[4].startswith('f__') else ''
    genus = parts[5].replace('g__', '') if len(parts) > 5 and parts[5].startswith('g__') else ''
    species = parts[6].replace('s__', '') if len(parts) > 6 and parts[6].startswith('s__') else ''
    
    return [kingdom, phylum, class_, order, family, genus, species]

def main():
    base_dir = input("Enter the base directory containing GCF folders: ")
    
    results = create_classification_dict(base_dir)
    
    output_file_path_1 = input("Enter the path to save the first output CSV file (e.g., snakemags1.csv): ")
    
    with open(output_file_path_1, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NZ_ID', 'Classification'])
        writer.writerows(results)

    df = pd.read_csv(output_file_path_1)
    
    final_results = []
    
    for _, row in df.iterrows():
        assembly_accession = row['NZ_ID']
        classification = row['Classification']
        
        taxonomy = split_classification(classification)
        
        final_results.append([assembly_accession] + taxonomy)

    output_file_path_2 = input("Enter the path to save the expanded output CSV file (e.g., snakemags_output.csv): ")
    
    with open(output_file_path_2, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NZ_ID', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'])
        writer.writerows(final_results)

    print(f"Output files created successfully: {output_file_path_1} and {output_file_path_2}")

if __name__ == "__main__":
    main()
