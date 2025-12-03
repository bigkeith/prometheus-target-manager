# prometheus-targets

This project aims to trivialize manually adding host to the prometheus targets list. 
while there are dynamic list with ansible they will pull more data than what is needed at this point. 
please feel free to extend this project in an way that you think it may help


## Getting started

included is a docker file and a docker compose.

the docker file is used to build the completed image while the docker compose

## To build the image
docker build -t prometheus-targets-app .
## To build and run
podman compose up

## If the image already exist you can run
podman run -v /path-to/targets.json:/app/files/targets.json:Z prometheus-targets-app

## portainer
the plan is to deploy from portainer so i created a stack:

##
version: '3.8'

services:
  prometheus-target-manager:
    image: localhost/prometheus-target-manager:latest
    container_name: prometheus-target-manager
    ports:
      - "5500:5000"
    volumes:
      - /etc/prometheus/targets.json:/app/files/targets.json:Z
    restart: unless-stopped
