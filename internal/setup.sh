#!/bin/bash

# Setup script for MLOps Assignment 2
# This script sets up the complete development environment

set -e  # Exit on error

echo "=========================================="
echo "MLOps Assignment 2 - Environment Setup"
echo "Group 126"
echo "=========================================="

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! python3 -c 'import sys; assert sys.version_info >= (3,9)' 2>/dev/null; then
    echo "Error: Python 3.9+ is required"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating project directories..."
mkdir -p data/train/cats data/train/dogs
mkdir -p data/validation/cats data/validation/dogs
mkdir -p data/test/cats data/test/dogs
mkdir -p models
mkdir -p logs
mkdir -p mlruns

echo "Directories created"

# Initialize Git if not already initialized
echo ""
echo "Checking Git repository..."
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: MLOps Assignment 2"
    echo "Git repository initialized"
else
    echo "Git repository already exists"
fi

# Initialize DVC if not already initialized
echo ""
echo "Checking DVC setup..."
if [ ! -d ".dvc" ]; then
    echo "Initializing DVC..."
    dvc init
    git add .dvc .dvcignore
    git commit -m "Initialize DVC"
    echo "DVC initialized"
else
    echo "DVC already initialized"
fi

# Check Docker
echo ""
echo "Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "Docker is installed: $(docker --version)"
else
    echo "Warning: Docker is not installed. Please install Docker Desktop."
fi

# Check kubectl
echo ""
echo "Checking kubectl installation..."
if command -v kubectl &> /dev/null; then
    echo "kubectl is installed: $(kubectl version --client --short 2>/dev/null || kubectl version --client)"
else
    echo "Warning: kubectl is not installed. Install if you plan to deploy to Kubernetes."
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Download the Cats vs Dogs dataset from Kaggle"
echo "2. Place images in data/ directory following the structure:"
echo "   data/train/cats/, data/train/dogs/, etc."
echo "3. Run: python src/train.py --epochs 20"
echo "4. Test locally: docker-compose up --build"
echo ""
echo "To activate the virtual environment in future:"
echo "  source venv/bin/activate"
echo ""
echo "Happy coding!"
echo "=========================================="
