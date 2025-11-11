#!/bin/bash

# Azure App Service Startup Script for Django
# This script runs when the container starts

echo "Starting PrantiX Django Application..."

# Set Python path
export PYTHONPATH=/home/site/wwwroot:$PYTHONPATH

# Install dependencies (in case of any updates)
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (with --noinput to avoid prompts)
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=prantix.settings

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput --settings=prantix.settings

# Start Gunicorn with deployment settings
echo "Starting Gunicorn web server..."
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=2 --worker-class=sync prantix.wsgi:application
