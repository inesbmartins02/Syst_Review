import os
import subprocess
import shutil

def activate_conda_env():
    """Activate the Conda environment."""
    cmd = """
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate SqueezeMeta
    """
    try:
        subprocess.run(cmd, shell=True, check=True, executable='/bin/bash')
        print("Conda environment 'SqueezeMeta' activated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error activating Conda environment: {e}")
        raise

def run_squeezemeta(sample_name, squeezemeta_path, input_dir, assembly_file):
    """
    Run SqueezeMeta tool and move the output to a specified directory.
    """
    
    # Use the sample name provided by the user
    output_dir = os.path.join(squeezemeta_path, sample_name, "results")
    final_output_dir = input("Enter the path to the final output directory: ")
    
    # Ensure the final output directory exists
    os.makedirs(final_output_dir, exist_ok=True)

    # Change to the SqueezeMeta directory
    os.chdir(squeezemeta_path)

    # Create samples.txt file using the user-defined sample name
    samples_file_path = os.path.join(squeezemeta_path, f"{sample_name}.txt")
    with open(samples_file_path, 'w') as samples_file:
        samples_file.write(f"{sample_name}\tcombined_viralgenomes.fasta\tpair1\n")
    
    print(f"Created {samples_file_path} with the necessary content.")

    # Command to execute SqueezeMeta with Conda activation
    cmd = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate SqueezeMeta
    ./SqueezeMeta.pl -m sequential -s {samples_file_path} -f {input_dir} -t 12 -extassembly {assembly_file}
    '
    """
    
    try:
        # Execute SqueezeMeta
        print("Running SqueezeMeta...")
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print output
        print("SqueezeMeta output:")
        print(result.stdout)
        
        # Print error output (if any)
        if result.stderr:
            print("SqueezeMeta stderr:")
            print(result.stderr)
        
        print("SqueezeMeta executed successfully.")
        
        # Move the output to the final directory
        print(f"Moving output to {final_output_dir}...")
        if os.path.exists(output_dir):
            for item in os.listdir(output_dir):
                s = os.path.join(output_dir, item)
                d = os.path.join(final_output_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            print(f"Output successfully moved to {final_output_dir}")
        else:
            print(f"Error: Output directory {output_dir} not found.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing SqueezeMeta: {e}")
        print(f"Error output: {e.stderr}")
        
    except FileNotFoundError:
        print("Error: SqueezeMeta command not found. Make sure SqueezeMeta is installed and in the correct directory.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    sample_name = input("Please enter the sample name: ")
    
    # User inputs for paths
    squeezemeta_path = input("Enter the path to the SqueezeMeta scripts directory: ")
    
    input_dir = input("Enter the path to the input directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/database/refdb/viral): ")
    
    assembly_file = input("Enter the path to the assembly file (e.g., combined_viralgenomes.fasta): ")
    
    run_squeezemeta(sample_name, squeezemeta_path, input_dir, assembly_file)
