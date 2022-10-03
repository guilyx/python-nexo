#!/usr/bin/env bash

set -e
source .env

if [ ${TESTING} = "true" ]
then
    pytest-3
else
    cd src 
    echo "Running Python App..."
    python3 main.py
fi
