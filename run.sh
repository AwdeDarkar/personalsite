#!/bin/sh

docker container stop personalsitedev || true && docker container rm personalsitedev || true
docker run -d --name personalsitedev -p 5001:5000 personalsitedev
