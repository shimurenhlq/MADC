#!/bin/bash

# MADC Framework - Environment Setup Script
# This script sets up the environment for running MADC experiments

set -e

echo "========================================="
echo "MADC Framework - Environment Setup"
echo "========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p data
mkdir -p results
mkdir -p logs

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env template..."
    cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Experiment Configuration
DATASET_PATH=./data
OUTPUT_DIR=./results
LOG_DIR=./logs
EOF
    echo ".env template created. Please update it with your API credentials."
else
    echo ".env file already exists."
fi

echo "========================================="
echo "Setup completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Update .env file with your API credentials"
echo "2. Update config.yaml with your experiment settings"
echo "3. Run: bash run_experiment.sh"
echo ""
