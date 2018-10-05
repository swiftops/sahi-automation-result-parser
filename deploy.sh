#!/bin/bash
export HOST_IP=10.0.2.250
cd /home/ubuntu/microservice
docker-compose scale sahiautomation=0
docker rm $(docker ps -q -f status=exited)
docker rmi -f swiftops/sahi_automation && docker pull swiftops/sahi_automation:latest && docker-compose up -d --remove-orphans
