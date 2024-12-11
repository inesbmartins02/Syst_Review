import os
import subprocess

def run_phyloflash():
    """
    Run PhyloFlash tool.
    
    Note: Before running this function, ensure that:
    1. The Conda environment 'pf' is created and properly set up.
    2. The required tools (barrnap, bedtools, seqtk, phyloFlash) are installed and accessible.
    3. The input FASTA file is in the correct location.
    """

    # User-defined paths
    input = input("Enter the path to the input FASTA file (e.g., combined_bacteria_sequences.fasta): ")
    gff_output = input("Enter the name for the GFF output file (e.g., all_bacteria_rRNA.gff): ")
    fasta_output = input("Enter the name for the FASTA output file (e.g., all_bacteria_16S.fa): ")
    fragmented_output = input("Enter the name for the fragmented output file (e.g., all_bacteria_16S_fragmented_250.fasta): ")
    
    # Commands to be executed
    commands = [
        f"barrnap --kingdom bac --threads 16 {input} > {gff_output}",
        f"bedtools getfasta -fi {input} -bed {gff_output} -fo {fasta_output}",
        f"seqtk seq -A {fasta_output} | seqtk trimfq -L 250 - | seqtk sample - 100000 > {fragmented_output}",
        f"phyloFlash.pl -lib SEQTESTE1 -CPUs 16 -read1 {fragmented_output} -dbhome /mnt/storagelv/home/inesbrancomartins/Tese/tools/phyloFlash/138.1"
    ]
    
    # Change to the PhyloFlash directory
    phyloflash_path = input("Enter the path to the PhyloFlash directory: ")
    os.chdir(phyloflash_path)

    # Command to activate the Conda environment
    conda_cmd = """
    bash -c '
    source ~/.bashrc
    eval "$(conda shell.bash hook)"
    conda activate pf
    """
    
    try:
        for command in commands:
            full_cmd = f"{conda_cmd} {command}'"
            print(f"Running command: {command}")
            result = subprocess.run(full_cmd, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Print command output
            print("Command output:")
            print(result.stdout)
            
            # Print error output if any
            if result.stderr:
                print("Command stderr:")
                print(result.stderr)
        
        print("PhyloFlash executed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        
    except FileNotFoundError:
        print("Error: Command not found. Make sure all tools are installed and in the correct directory.")

if __name__ == "__main__":
    print("IMPORTANT: Make sure the Conda environment 'pf' is set up and the input files are in place.")
    input("Press Enter to continue or Ctrl+C to cancel...")
    run_phyloflash()
