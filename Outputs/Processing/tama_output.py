import csv

def main():
    mapping_file = input("Enter the path to the GCF sequence ID mapping file (e.g., archaea_gcf_sequence_id_mapping.csv): ")
    tama_output_file = input("Enter the path to the TAMA output file (e.g., read_classi.out): ")
    output_csv = input("Enter the path to save the new CSV file (e.g., tama_output.csv): ")

    sequence_to_gcf = {}
    with open(mapping_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            gcf_id, sequence_id = row
            sequence_to_gcf[sequence_id] = gcf_id

    with open(tama_output_file, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
        writer.writerow(['GCF_ID', 'Taxon_ID']) 

        for line in infile:
            sequence_id, taxon_id, _ = line.strip().split('\t')
            gcf_id = sequence_to_gcf.get(sequence_id)
            
            if gcf_id and taxon_id != 'NA':
                taxon_id = taxon_id.replace('"', '')  
                writer.writerow([gcf_id, taxon_id])

    print(f"Output CSV created successfully: {output_csv}")

if __name__ == "__main__":
    main()
