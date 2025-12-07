#!/bin/bash

# Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping generation."
else
    echo "Please enter your Google Gemini API Key:"
    read -r api_key
    echo "GEMINI_API_KEY=$api_key" > .env
    echo ".env file created."
fi

echo "Setup complete. You can now run the game using ./run.sh"
