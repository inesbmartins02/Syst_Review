import os
import subprocess
import shutil

def run_viwrap():
    """
    Run ViWrap tool using geNomad and move the output to a specified directory.
    
    Note: Before running this function, ensure that:
    1. The Conda environment 'ViWrap-geNomad' is created and properly set up.
    2. The ViWrap tool is installed and accessible.
    3. The input files and directories are in the correct locations.
    """
    
    # User-defined paths
    input_file = input("Enter the path to the input FASTA file (e.g., combined_viral_sequences.fasta): ")
    output_dir = input("Enter the path to the output directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/tools/ViWrap/results/genomad_output): ")
    genomad_db = input("Enter the path to the geNomad database (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/tools/ViWrap/ViWrap_db/genomad_db/genomad_db): ")
    final_output_dir = input("Enter the path to the final output directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/outputs/viwrap): ")

    # Ensure the final output directory exists
    os.makedirs(final_output_dir, exist_ok=True)

    # Command to activate the Conda environment and execute geNomad
    cmd = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate ViWrap-geNomad
    genomad end-to-end {input_file} {output_dir} {genomad_db} --threads 4 --conservative-taxonomy
    '
    """
    
    try:
        # Execute geNomad
        print("Running geNomad...")
        result = subprocess.run(cmd, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print output
        print("geNomad output:")
        print(result.stdout)
        
        # Print error output (if any)
        if result.stderr:
            print("geNomad stderr:")
            print(result.stderr)
        
        print("geNomad executed successfully.")
        
        # Move the output to the final directory
        print(f"Moving output to {final_output_dir}...")
        for item in os.listdir(output_dir):
            s = os.path.join(output_dir, item)
            d = os.path.join(final_output_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        
        print(f"Output successfully moved to {final_output_dir}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing geNomad: {e}")
        print(f"Error output: {e.stderr}")
        
    except FileNotFoundError:
        print("Error: geNomad command not found. Make sure it's installed and in the correct directory.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("IMPORTANT: Make sure the Conda environment 'ViWrap-geNomad' is set up and all required files are in place.")
    input("Press Enter to continue or Ctrl+C to cancel...")
    run_viwrap()
