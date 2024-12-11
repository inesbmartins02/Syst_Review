import pandas as pd

def main():
    input_file = input("Enter the path to the input file (e.g., archaea.microbe_stat_by_sequence_id_assembly_info): ")
    output_file = input("Enter the path to save the output CSV file: ")

    try:
        df = pd.read_csv(input_file, sep='\t')  
    except pd.errors.ParserError as e:
        print(f"Error reading the file: {e}")
        exit()
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit()

    required_columns = ['assembly_id', 'sequence_id', 'genus_tax_name', 'species_tax_name']
    if not all(col in df.columns for col in required_columns):
        print("One or more required columns are missing in the file.")
        exit()

    selected_columns = df[required_columns]

    selected_columns.rename(columns={
        'genus_tax_name': 'Genus',
        'species_tax_name': 'Species'
    }, inplace=True)

    try:
        selected_columns.to_csv(output_file, index=False)
        print(f"File processed and saved as {output_file}.")
    except Exception as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    main()
