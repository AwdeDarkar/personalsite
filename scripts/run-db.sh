#!/bin/sh

docker container stop postgresben || true && docker container rm postgresben || true
docker run --name postgresben -e POSTGRES_PASSWORD=$FLASK_DATABASE_PASS \
    -v $POSTGRES_PERSISTANT_DATA_DIRECTORY:/var/lib/postgresql/data \
    -d postgres
docker network connect \
    --ip 172.10.0.20 \
    personalsite postgresben
