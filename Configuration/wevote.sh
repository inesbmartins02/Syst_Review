#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Clone the WEVOTE-strain repository
echo "Cloning WEVOTE-strain repository..."
git clone https://github.com/aametwally/WEVOTE-strain.git

# Change to the WEVOTE-strain directory
echo "Changing to WEVOTE-strain directory..."
cd WEVOTE-strain

# Make all shell scripts executable
echo "Setting executable permissions for shell scripts..."
chmod +x *.sh

echo "Installation complete. WEVOTE-strain is ready to use."
