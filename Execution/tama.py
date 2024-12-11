import subprocess
import os

def run_tama(output_dir, param_file, threads):
    """
    Run the TAMA tool.

    Args:
    output_dir (str): Directory for output results.
    param_file (str): Parameter file for TAMA.
    threads (int): Number of threads to use.
    """
    # Directory where TAMA is located
    tama_dir = input("Enter the path to the TAMA directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/tools/TAMA): ")

    # Change to the TAMA directory
    original_dir = os.getcwd()
    os.chdir(tama_dir)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Construct the TAMA command
    tama_command = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate tama_env
    perl ./TAMA.pl -p {threads} -o {output_dir} --param {param_file} -t True
    '
    """

    try:
        # Run the TAMA command
        subprocess.run(tama_command, shell=True, check=True, executable='/bin/bash')
        print("TAMA execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running TAMA: {e}")
    except FileNotFoundError:
        print("Error: TAMA.pl not found. Make sure it's in the TAMA directory.")
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    # User inputs for paths and parameters
    output_dir = input("Enter the output directory for results (e.g., ./TAMAout): ")
    param_file = input("Enter the path to the parameter file (e.g., ./params): ")
    threads = int(input("Enter the number of threads to use (e.g., 20): "))

    run_tama(output_dir, param_file, threads)
