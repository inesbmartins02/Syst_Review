import subprocess
import os

def run_camitax():
    """
    Run CAMITAX tool using Nextflow.
    
    Note: Before running this function, ensure that:
    1. The Conda environment 'camitax_env' is created and properly set up.
    2. The CAMITAX tool is installed and accessible.
    3. The input files and directories are in the correct locations.
    """
    
    # User-defined paths
    db_path = input("Enter the path to the CAMITAX database directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/tools/CAMITAX/db): ")
    input_dir = input("Enter the path to the input directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/database/refdb/fungi/outputGCFfiltrado/): ")
    
    # Command to activate the Conda environment and execute CAMITAX
    cmd = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate camitax_env
    nextflow run CAMI-challenge/CAMITAX -profile docker --db {db_path} --i {input_dir} --x fna
    '
    """
    
    try:
        # Execute CAMITAX
        print("Running CAMITAX...")
        result = subprocess.run(cmd, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print output
        print("CAMITAX output:")
        print(result.stdout)
        
        # Print error output (if any)
        if result.stderr:
            print("CAMITAX stderr:")
            print(result.stderr)
        
        print("CAMITAX executed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing CAMITAX: {e}")
        print(f"Error output: {e.stderr}")
        
    except FileNotFoundError:
        print("Error: CAMITAX command not found. Make sure it's installed and in the correct directory.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("IMPORTANT: Make sure the Conda environment 'camitax_env' is set up and all required files are in place.")
    input("Press Enter to continue or Ctrl+C to cancel...")
    run_camitax()
import subprocess
import os

def run_camitax():
    """
    Run CAMITAX tool using Nextflow.
    
    Note: Before running this function, ensure that:
    1. The Conda environment 'camitax_env' is created and properly set up.
    2. The CAMITAX tool is installed and accessible.
    3. The input files and directories are in the correct locations.
    """
    
    # User-defined paths
    db_path = input("Enter the path to the CAMITAX database directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/tools/CAMITAX/db): ")
    input_dir = input("Enter the path to the input directory (e.g., /mnt/storagelv/home/inesbrancomartins/Tese/database/refdb/fungi/outputGCFfiltrado/): ")
    
    # Command to activate the Conda environment and execute CAMITAX
    cmd = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate camitax_env
    nextflow run CAMI-challenge/CAMITAX -profile docker --db {db_path} --i {input_dir} --x fna
    '
    """
    
    try:
        # Execute CAMITAX
        print("Running CAMITAX...")
        result = subprocess.run(cmd, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print output
        print("CAMITAX output:")
        print(result.stdout)
        
        # Print error output (if any)
        if result.stderr:
            print("CAMITAX stderr:")
            print(result.stderr)
        
        print("CAMITAX executed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing CAMITAX: {e}")
        print(f"Error output: {e.stderr}")
        
    except FileNotFoundError:
        print("Error: CAMITAX command not found. Make sure it's installed and in the correct directory.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("IMPORTANT: Make sure the Conda environment 'camitax_env' is set up and all required files are in place.")
    input("Press Enter to continue or Ctrl+C to cancel...")
    run_camitax()
