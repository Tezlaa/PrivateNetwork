#!/bin/bash

# Check the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # On Linux
    
    echo "Created venv..."
    python3 -m venv venv

    echo "Install requirements..."
    source venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt

    echo "Rename file. Migrate files..."
    mv .env_copy .env
    cd src/
    python3 manage.py migrate

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # On Windows (Git Bash, Cygwin, or MSYS)

    echo "Created venv..."
    python -m venv venv

    echo "Install requirements..."
    . venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    echo "Rename file. Migrate files..."
    mv .env_copy .env
    cd src/
    python manage.py migrate
  
else
    echo "Unsupported operating system..."
fi
    echo "Final setup."

# Keep the terminal open
bash