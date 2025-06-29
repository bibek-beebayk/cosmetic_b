#!/bin/bash

# Navigate to your Django project directory
cd /home/ubuntu/blackvilla-be

# Activate your virtual environment (adjust the path)
source /home/ubuntu/env/bin/activate

# Pull the latest code from your repository
git pull origin main

# Install or update Python dependencies
pip install -r requirements/prod.txt

# Run Django database migrations
./manage.py migrate

# Collect static files (if needed)
./manage.py collectstatic --noinput

# Restart your application server (e.g., Gunicorn)
sudo systemctl restart blackvilla-be.service

# Restart Nginx (if you made changes to Nginx configuration)
sudo systemctl restart nginx

# Deactivate the virtual environment
deactivate
