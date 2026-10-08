#!/bin/bash
# Build script for Vercel deployment

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Applying database migrations..."
python3 manage.py migrate --noinput

echo "Seeding initial demo data..."
python3 manage.py seed_foodflow_demo

echo "Build process completed successfully!"
