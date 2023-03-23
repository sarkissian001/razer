#!/bin/bash

DIR_NAME="/core/modules/razer_dagster_manager"

# Navigate to the project root directory
cd "$(git rev-parse --show-toplevel)"


# Check if running in a virtual environment
if [ -d "venv" ] || [ -d "env" ]; then
    echo "Building package in existing virtual environment."
    source venv/bin/activate || source env/bin/activate
else
    echo "It looks like you're not currently using a virtual environment."
    read -p "Would you like to create and activate a virtual environment now? (y/n) " choice
    case "$choice" in
      y|Y )
        python -m venv venv
        source venv/bin/activate
        ;;
      n|N )
        echo "Please activate a virtual environment and run this script again."
        exit 1
        ;;
      * )
        echo "Invalid choice. Please try again."
        exit 1
        ;;
    esac
fi


# Change dir

cd "$(git rev-parse --show-toplevel)$DIR_NAME"


# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build the module
python3 setup.py sdist bdist_wheel

echo "installing .whl package"
pip install dist/*.whl --force-reinstall


# Remove the build directory
rm -rf ./build
