#!/bin/sh

if [[ $1 = "dev" ]]; then
    source dev_env
    python3 manage.py run
else
    source prod_env
fi
