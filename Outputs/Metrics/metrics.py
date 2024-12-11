import subprocess
import os

def run_scripts():
    script_directory = input("Enter the directory where the scripts are located: ")

    scripts = [
        'metrics_phabox.py',
        'metrics_basta.py',
        'metrics_viwrap.py',
        'metrics_squeezemeta.py',
        'metrics_camitax.py',
        'metrics_snakemags.py',
        'metrics_tama.py',
        'metrics_phyloflash.py',
        'metrics_mpn.py'
    ]

    print(f"Executing {scripts[0]}...")
    subprocess.run(['python3', os.path.join(script_directory, scripts[0])])

    processes = []
    for script in scripts[1:]:
        print(f"Starting {script}...")
        process = subprocess.Popen(['python3', os.path.join(script_directory, script)])
        processes.append(process)

    for process in processes:
        process.wait()

    print("All scripts have been executed.")

if __name__ == "__main__":
    run_scripts()
