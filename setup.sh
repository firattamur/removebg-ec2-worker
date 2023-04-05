#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y git python3-pip

# Navigate to the uploaded code directory
cd /home/ubuntu/removebg-worker

# Install any required packages (if you have a requirements.txt file)
pip3 install -r requirements.txt

# Run your code
python3 src/main.py