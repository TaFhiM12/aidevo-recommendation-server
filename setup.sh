#!/bin/bash

# Aidevo Recommendation Service - Setup Script
# Automates the setup process

set -e

echo "======================================"
echo "Aidevo Recommendation Service Setup"
echo "======================================"

# Check Python
echo -e "\n[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
echo -e "\n[2/6] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo -e "\n[3/6] Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Setup .env file
echo -e "\n[4/6] Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created from template"
    echo "⚠ Please edit .env with your MongoDB connection string"
    echo "   Run: nano .env"
else
    echo "✓ .env file already exists"
fi

# Generate dataset
echo -e "\n[5/6] Generating dataset..."
echo "This may take a moment..."
python scripts/generate_dataset.py

# Train models
echo -e "\n[6/6] Training models..."
python scripts/train_model.py

echo -e "\n======================================"
echo "✓ Setup completed successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Start the service: python -m app.main"
echo "2. Visit API docs: http://localhost:5000/docs"
echo "3. Test endpoint: curl http://localhost:5000/health"
echo ""
