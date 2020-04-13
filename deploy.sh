#!/bin/bash

if [[ $1 = "dev" ]]; then
    ./scripts/build-dev.sh
    ./scripts/run-dev.sh
else
    ./scripts/build-prod.sh
    ./scripts/run-prod.sh
fi
