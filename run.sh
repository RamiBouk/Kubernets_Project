#!/bin/bash

# Project 1: classifier
echo "Entering classifier environment..."
cd ./classifier
source venv/bin/activate

# Run Python files
python classify.py &
python server.py &

# Project 2: database
echo "Entering database environment..."
cd ../database
source venv/bin/activate

# Run Python files
python server.py &

# Project 3: interface
echo "Entering interface environment..."
cd ../interface
source venv/bin/activate

# Run Python files
python main.py &

# Wait for all processes to finish
wait

# Deactivate virtual environments
deactivate  # classifier
deactivate  # database
deactivate  # interface

