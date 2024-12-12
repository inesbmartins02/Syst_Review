### README

#### Systematic Review of Metagenomic Tools

This systematic review evaluates the performance of nine selected metagenomic tools: **BASTA**, **Camitax**, **MegaPath-Nano**, **PhaBOX**, **PhyloFlash**, **SqueezeMeta**, **SnakeMAGs**, **ViWrap**, and **TAMA**.

### Repository Organization

The files in this GitHub repository are organized into four different folders, each corresponding to a specific testing process.

#### Configuration
- This folder contains configuration and installation files for the 31 tools used in the review. These files are Bash scripts.

#### Database
- This folder includes scripts to install and prepare all necessary data to replicate the work using our dataset.
  - **Prerequisites**:
    - Before running the scripts in this folder, users need to download the assembly files (`assembly_files.txt`) for each domain from the NCBI FTP site.
  - **Scripts**:
    - **`create_database.py`**: Downloads 10% of the content from each assembly file and organizes the datasets by domain.
    - **`extractNC.py`**: Maps the content of each Genome Collection File (GCF) with its respective sequence identifiers.
    - **`extractTaxonomy.py`**: Creates a CSV file containing the GCF and its respective taxonomy, organized by domains.
    - Additional scripts modify the data format and organization, including:
      - Implementing mutations
      - Converting formats (e.g., FASTA to FASTQ)
      - Formatting into paired-end reads
    - **`GCFtocombinedfasta.py`**: Combines all GCFs from each domain into a single FASTA file, separating sequences by identifier. This script is used as input for most of the tools.

#### Execution
- This folder contains execution files for each tool tested. Each script includes steps for input transformation, environment activation, and execution commands.
  - **User Input Required**:
    - Users must insert the path to the installation directory of the tool, the input file, and the desired output directory in each script.
  - **Important Note**:
    - These tools must be executed in isolation to avoid overloading the system.

#### Outputs
- The outputs folder contains two subfolders: **Processing** and **Metrics**.
  
  ##### Processing
  - This folder contains nine transformation files that convert the outputs from each tool into a format compatible with the CSV file generated during the Database step for taxonomy comparison.

  ##### Metrics
  - After all outputs have been properly configured, execute `main.py` in this folder to obtain performance metrics such as F1 score, precision, and recall for each taxonomic level of each tool.

### Usage

1. **Download Assembly Files**:
   - Go to the NCBI FTP site and download the assembly files (`assembly_files.txt`) for each domain.

2. **Run Database Scripts**:
   - Execute `create_database.py` to download and organize the datasets.
   - Run `extractNC.py` to map GCF content with sequence identifiers.
   - Run `extractTaxonomy.py` to create a CSV file with GCF and taxonomy information.
   - Use additional scripts as needed to modify data formats.

3. **Prepare Input Files**:
   - Use `GCFtocombinedfasta.py` to combine GCFs into a single FASTA file for each domain.

4. **Run Tools**:
   - Navigate to the `Execution` folder.
   - For each tool, edit the script to include the following paths:
     - Path to the tool's installation directory
     - Path to the input file
     - Path to the desired output directory
   - Execute the script for each tool in isolation to avoid system overload.

5. **Process Outputs**:
   - Move to the `Outputs/Processing` folder and ensure all transformation files are correctly set up.
   - After processing, navigate to `Outputs/Metrics`.

6. **Calculate Metrics**:
   - Run `main.py` in the Metrics folder to calculate F1 score, precision, and recall for each taxonomic level across all tools.

### Contributing

Contributions are welcome. Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

### License

This project is licensed under [LICENSE](LICENSE). Please review the license terms before using or distributing the code.

### Acknowledgments

We acknowledge the contributions of all authors and the resources used in this systematic review. For more details, please refer to our publication.

---

By following these steps, you can replicate our work and evaluate the performance of these metagenomic tools using our dataset. If you have any questions or need further assistance, please open an issue in this repository.
