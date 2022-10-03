#!/usr/bin/env bash

set -e
source .env

if [ ${TESTING} = "true" ]
then
    pytest-3
else
    tail -f /dev/null
fi
