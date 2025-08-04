#!/bin/bash

# Install qpdf on startup
apt-get update && apt-get install -y qpdf

# Start your Flask app
python app.py
