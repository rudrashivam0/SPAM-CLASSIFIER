 #!/bin/bash

# Exit script on any error
set -e

# Update package lists
echo "Updating package lists..."
sudo apt update -y

# Install Python 3 and pip if not already installed
echo "Checking Python3 installation..."
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found, installing..."
    sudo apt install python3 -y
fi

echo "Checking pip installation..."
if ! command -v pip3 &>/dev/null; then
    echo "pip3 not found, installing..."
    sudo apt install python3-pip -y
fi

# Install virtualenv if not already installed
echo "Checking virtualenv installation..."
if ! pip3 show virtualenv &>/dev/null; then
    echo "virtualenv not found, installing..."
    pip3 install virtualenv
fi

# Create a virtual environment
echo "Creating virtual environment..."
virtualenv env

# Activate the virtual environment
echo "Activating virtual environment..."
source env/bin/activate

# Install required Python packages
echo "Installing Python dependencies..."
pip install streamlit nltk scikit-learn

# Download NLTK data
echo "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Setup complete. Use 'source env/bin/activate' to activate the virtual environment and 'streamlit run <script>.py' to run your app."
