#!/bin/bash
# AIVI - Quick Start with Virtual Environment

echo "🚀 Starting AIVI with Virtual Environment..."
echo ""

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if activation was successful
if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated"
else
    echo "❌ Failed to activate virtual environment"
    echo "Please run: python -m venv venv"
    exit 1
fi

echo ""
echo "🎨 Launching AIVI..."
echo ""

# Launch the application
python splash_launcher.py

# Deactivate on exit
deactivate
