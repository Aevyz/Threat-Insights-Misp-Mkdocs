#!/bin/bash
# Quick setup script for HvS Threat Insights MkDocs

set -e

echo "🚀 Setting up HvS Threat Insights MkDocs..."
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Fetch data: python fetch_data.py"
echo "  3. Build docs: python build.py"
echo "  4. Serve locally: mkdocs serve"
echo ""
