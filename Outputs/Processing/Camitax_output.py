import csv

def transform_camitax_output(camitax_file, output_file):
    with open(camitax_file, 'r') as f:
        camitax_data = [line.strip().split('\t') for line in f if line.strip()]

    transformed_data = []

    for entry in camitax_data:
        accession_id = entry[0].replace('_genomic', '')  
        taxid = entry[1]
        classification_value = entry[2]  
        classification_level = entry[3]  

        kingdom = ''
        phylum = ''
        class_ = ''
        order = ''
        family = ''
        genus = ''
        species = ''

        if classification_level == 'superkingdom':
            kingdom = classification_value
        elif classification_level == 'phylum':
            phylum = classification_value
        elif classification_level == 'class':
            class_ = classification_value
        elif classification_level == 'order':
            order = classification_value
        elif classification_level == 'family':
            family = classification_value
        elif classification_level == 'genus':
            genus = classification_value
        elif classification_level == 'species':
            species = classification_value

        transformed_row = [
            accession_id,
            'Archaea' if taxid == '2157' else ('Bacteria' if taxid == '2' else ''),
            kingdom,
            phylum,
            class_,
            order,
            family,
            genus,
            species or ''  
        ]
        
        transformed_data.append(transformed_row)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['accession', 'domain', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'])  # Header
        writer.writerows(transformed_data)

def main():
    camitax_output_file = input("Enter the path to the CAMITAX output file (e.g., camitax.tsv): ")
    output_transformed_file = input("Enter the path to save the transformed output CSV file: ")

    transform_camitax_output(camitax_output_file, output_transformed_file)

    print(f"Data transformed and saved in {output_transformed_file}")

if __name__ == "__main__":
    main()
