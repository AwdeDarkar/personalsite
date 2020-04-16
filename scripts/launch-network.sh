#!/bin/sh

for i in ` docker network inspect -f '{{range .Containers}}{{.Name}} {{end}}' personalsite`;\
  do \
     docker network disconnect -f personalsite $i; \
  done;
docker network rm personalsite
docker network create \
    --driver=bridge \
    --subnet=172.10.0.0/16 \
    personalsite
