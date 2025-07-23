#! /bin/bash

docker stop shakespeare-x-server
docker rm shakespeare-x-server
docker build -t shakespeare-x-server .
docker run -p 8000:8000 -d --name=shakespeare-x-server shakespeare-x-server
