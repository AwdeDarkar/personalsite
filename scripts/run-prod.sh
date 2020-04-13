#!/bin/sh

docker container stop personalsiteprod || true && docker container rm personalsiteprod || true
docker run -d --name personalsiteprod -p 5000:5000 personalsiteprod
