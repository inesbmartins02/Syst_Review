import os
import subprocess
import shutil

def run_metagenomic_pipeline(input_data, basta_path, output_dir, ref_db, blast_db):
    """
    Run the complete metagenomic pipeline including BLAST and BASTA,
    and move the output to a specified directory.

    Parameters:
    - input_data: Path to the input file (e.g., combined_viralgenomes.fasta)
    - basta_path: Path to the BASTA directory
    - output_dir: Path to the output directory
    - ref_db: Path to the reference database (e.g., uniprot_sprot.fasta)
    - blast_db: Name of the BLAST database (e.g., uniprot_sprot)
    """

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Copy the input file to the BASTA directory
    input_filename = os.path.basename(input_data)
    destination = os.path.join(basta_path, input_filename)
    shutil.copy(input_data, destination)

    # Change to the BASTA directory
    os.chdir(basta_path)

    # Command to run BLAST
    blast_cmd = f"blastx -query {input_filename} -db {blast_db} -out resultados_blast_virus.txt -outfmt \"6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore\""

    # Command to run BASTA (adjust according to specific BASTA needs)
    basta_cmd = "basta sequence resultados_blast_virus.txt resultados_basta_virus uni"

    try:
        # Run BLAST
        print("Running BLAST...")
        blast_result = subprocess.run(blast_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("BLAST output:")
        print(blast_result.stdout)

        if blast_result.stderr:
            print("BLAST stderr:")
            print(blast_result.stderr)

        print("BLAST executed successfully.")

        # Run BASTA
        print("\nRunning BASTA...")
        basta_result = subprocess.run(basta_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("BASTA output:")
        print(basta_result.stdout)

        if basta_result.stderr:
            print("BASTA stderr:")
            print(basta_result.stderr)

        print("BASTA executed successfully.")

        # Move the output file to the specified directory
        output_file = "resultados_basta_virus"
        if os.path.exists(output_file):
            shutil.move(output_file, os.path.join(output_dir, output_file))
            print(f"Moved {output_file} to {output_dir}")
        else:
            print(f"Warning: {output_file} not found. Check if BASTA generated the output file.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
    except FileNotFoundError:
        print("Error: Command not found. Make sure BLAST and BASTA are installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Starting metagenomic pipeline...")

    # User configurations
    input_data = input("Enter the path to the input file (e.g., combined_viralgenomes.fasta): ")
    basta_path = input("Enter the path to the BASTA directory: ")
    output_dir = input("Enter the path to the output directory: ")
    ref_db = input("Enter the path to the reference database (e.g., uniprot_sprot.fasta): ")
    blast_db = input("Enter the name of the BLAST database (e.g., uniprot_sprot): ")

    run_metagenomic_pipeline(input_data, basta_path, output_dir, ref_db, blast_db)

# Notes and Help
"""
## Input Format
- **input_data**: Path to the input file (FASTA format).
- **basta_path**: Path to the BASTA directory.
- **output_dir**: Path to the output directory.
- **ref_db**: Path to the reference database (FASTA format).
- **blast_db**: Name of the BLAST database.

## Output Location
- The output file will be moved to the directory specified in **output_dir**.

## Example Usage
- Run the script and follow the instructions to insert the paths and names of the necessary files.
"""
