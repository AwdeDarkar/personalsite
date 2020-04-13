#!/bin/sh

docker container stop personalsitedev || true && docker container rm personalsitedev || true
docker run -d --name personalsitedev -p 5000:5000 personalsitedev
