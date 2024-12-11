import os
import subprocess

def run_snakemags():
    """
    Run SnakeMAGs tool using the specified configuration.
    
    Note: Before running this function, ensure that:
    1. The Conda environment 'snakemake' is created and properly set up.
    2. The SnakeMAGs tool is installed and accessible.
    3. The config.yaml file is properly configured.
    """
    
    # User-defined paths
    config_path = input("Enter the path to the config.yaml file: ")
    snakefile_path = input("Enter the path to the SnakeMAGs Snakefile (e.g., SnakeMAGs.smk): ")
    conda_prefix = input("Enter the path to the Conda environment prefix (e.g., /path/to/conda/env): ")
    
    # Command to activate the Conda environment and execute SnakeMAGs
    cmd = f"""
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate snakemake
    snakemake --cores 30 \
               --snakefile {snakefile_path} \
               --use-conda \
               --conda-prefix {conda_prefix} \
               --configfile {config_path} \
               --keep-going \
               --latency-wait 180 \
               --rerun-incomplete
    '
    """
    
    try:
        # Execute SnakeMAGs
        print("Running SnakeMAGs...")
        result = subprocess.run(cmd, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print output
        print("SnakeMAGs output:")
        print(result.stdout)
        
        # Print error output (if any)
        if result.stderr:
            print("SnakeMAGs stderr:")
            print(result.stderr)
        
        print("SnakeMAGs executed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing SnakeMAGs: {e}")
        print(f"Error output: {e.stderr}")
        
    except FileNotFoundError:
        print("Error: SnakeMAGs command not found. Make sure it's installed and in the correct directory.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("IMPORTANT: Make sure the Conda environment 'snakemake' is set up and all required files are in place.")
    input("Press Enter to continue or Ctrl+C to cancel...")
    run_snakemags()
