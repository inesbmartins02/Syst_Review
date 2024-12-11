import os
import subprocess
import shutil

def run_mpn(mpn_path, final_output_dir, fasta_file):
    """
    Run MegaPathNano (mpn) tool and move the output to a specified directory.

    Note: Before running this function, ensure that:
    1. The Conda environment 'mpn' is created and properly set up.
    2. The MegaPathNano tool is installed in the specified directory.
    3. The input FASTA file is in the correct location.

    Parameters:
    - mpn_path: Path to the MegaPathNano directory
    - final_output_dir: Path to the final output directory
    - fasta_file: Path to the input FASTA file
    """

    # Ensure the final output directory exists
    os.makedirs(final_output_dir, exist_ok=True)

    # Define the temporary output directory
    output_dir = os.path.join(mpn_path, 'results')

    # Change to the MegaPathNano bin directory
    bin_path = os.path.join(mpn_path, 'bin')
    os.chdir(bin_path)

    # Command to activate the Conda environment and run MegaPathNano
    cmd = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate mpn
    python ../megapath_nano.py --query {fasta_file} --taxon_module_only --output_prefix minha_amostra --output_folder {output_dir} --max_aligner_thread 16
    '
    """

    try:
        # Run MegaPathNano
        print("Running MegaPathNano...")
        result = subprocess.run(cmd, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print MegaPathNano output
        print("MegaPathNano output:")
        print(result.stdout)

        # Print error output (which may contain important messages)
        if result.stderr:
            print("MegaPathNano stderr:")
            print(result.stderr)

        print("MegaPathNano executed successfully.")

        # Move the output to the final directory
        print(f"Moving output from {output_dir} to {final_output_dir}...")
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
        print(f"Error executing MegaPathNano: {e}")
        print(f"Error output: {e.stderr}")
    except FileNotFoundError:
        print("Error: MegaPathNano command not found. Make sure MegaPathNano is installed and in the correct directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("IMPORTANT: Make sure the Conda environment 'mpn' is set up and the input files are in place.")
    input("Press Enter to continue or Ctrl+C to cancel...")

    # User configurations
    mpn_path = input("Enter the path to the MegaPathNano directory: ")
    final_output_dir = input("Enter the path to the final output directory: ")
    fasta_file = input("Enter the path to the input FASTA file: ")

    run_mpn(mpn_path, final_output_dir, fasta_file)

# Notes and Help
"""
## Input Format
- **mpn_path**: Path to the MegaPathNano directory.
- **final_output_dir**: Path to the final output directory.
- **fasta_file**: Path to the input FASTA file.

## Output Location
- The output files will be moved from the temporary directory 'results' inside **mpn_path** to the directory specified in **final_output_dir**.

## Example Usage
- Run the script and follow the instructions to insert the paths and names of the necessary files.
"""
