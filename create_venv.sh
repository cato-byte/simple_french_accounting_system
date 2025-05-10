#!/bin/bash

# Script to create (if not already existent) and activate a Python virtual environment for a project

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip is not installed. Installing pip..."
    sudo apt-get update
    # install GUI
    sudo apt-get install python3-tk
    sudo apt-get install python3-pip
fi

# Define the name of the virtual environment directory
VENV_DIR="env_simple_french_accounting_system"

# Check if the virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment $VENV_DIR already exists."
else
    # Create a virtual environment
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source $VENV_DIR/bin/activate

# Check if requirements.txt exists and install packages
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping package installation."
fi

echo "Virtual environment is set up and activated."