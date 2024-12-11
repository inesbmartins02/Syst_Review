import os
import subprocess
import shutil
from Bio import SeqIO

def convert_fasta(input_file, output_file):
    """
    Convert FASTA file to the required format for PhaBOX2 and create an ID mapping.
    
    Returns a dictionary mapping new IDs to original IDs.
    """
    mapping = {}
    print(f"Converting FASTA file from {input_file} to {output_file}...")
    with open(output_file, 'w') as out_f:
        for i, record in enumerate(SeqIO.parse(input_file, "fasta")):
            new_id = f"{i + 1}"
            original_id = record.id
            mapping[new_id] = original_id
            out_f.write(f">{new_id}\n{record.seq}\n")
    
    print(f"Conversion complete. Output file: {output_file}")
    return mapping

def save_id_mapping(mapping, mapping_file):
    """
    Save the ID mapping to a TSV file.
    """
    print(f"Saving ID mapping to {mapping_file}...")
    with open(mapping_file, 'w') as f:
        f.write("New_ID\tOriginal_ID\n")
        for new_id, original_id in mapping.items():
            f.write(f"{new_id}\t{original_id}\n")
    print(f"ID mapping saved to: {mapping_file}")

def run_phabox(phabox_path, converted_fasta):
    """
    Run PhaBOX2 tool.
    
    Note: Before running this function, ensure that:
    1. The Conda environment 'phabox2' is created and properly set up.
    2. The PhaBOX2 tool is installed in the specified directory.
    3. The database directory 'phabox_db_v2.0.0' is present.
    """
    
    # Define output directories
    output_dir = os.path.join(phabox_path, 'results')
    
    # Ensure final output directory exists
    final_output_dir = input("Enter the path to the final output directory: ")
    os.makedirs(final_output_dir, exist_ok=True)

    # Change to the PhaBOX2 bin directory
    bin_path = os.path.join(phabox_path, 'bin')
    os.chdir(bin_path)

    # Command to activate Conda environment and run PhaBOX2
    cmd = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate phabox2
    python ../phabox2 --task phagcn --contigs {converted_fasta} --outpth {output_dir} --threads 40 --dbdir phabox_db_v2.0.0
    '
    """

    try:
        # Execute PhaBOX2
        print("Running PhaBOX2...")
        result = subprocess.run(cmd, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print PhaBOX2 output
        print("PhaBOX2 output:")
        print(result.stdout)
        
        # Print error output if any
        if result.stderr:
            print("PhaBOX2 stderr:")
            print(result.stderr)
        
        print("PhaBOX2 executed successfully.")
        
        # Move results to final output directory
        print(f"Moving output results from {output_dir} to {final_output_dir}...")
        for item in os.listdir(output_dir):
            s = os.path.join(output_dir, item)
            d = os.path.join(final_output_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
                print(f"Copied directory {s} to {d}")
            else:
                shutil.copy2(s, d)
                print(f"Copied file {s} to {d}")

        print(f"Output successfully moved to {final_output_dir}")

    except subprocess.CalledProcessError as e:
        print(f"Error executing PhaBOX2: {e}")
        print(f"Error output: {e.stderr}")
        
    except FileNotFoundError:
        print("Error: PhaBOX2 command not found. Make sure PhaBOX2 is installed and in the correct directory.")

if __name__ == "__main__":
    print("IMPORTANT: Make sure the Conda environment 'phabox2' is set up and the input files are in place.")
    
    # User inputs for paths
    phabox_path = input("Enter the path to the PhaBOX directory: ")
    
    input_file = input("Enter the path to the input FASTA file: ")
    
    converted_fasta = input("Enter the path for the converted FASTA output file: ")
    
    # Convert FASTA file and get ID mapping
    id_mapping = convert_fasta(input_file, converted_fasta)
    
    # Save ID mapping to a file
    mapping_file = input("Enter the path for saving ID mapping (e.g., /path/to/id_mapping.tsv): ")
    save_id_mapping(id_mapping, mapping_file)

    # Run PhaBOX with the converted FASTA file
    run_phabox(phabox_path, converted_fasta)
