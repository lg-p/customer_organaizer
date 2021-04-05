#!/bin/sh

docker-compose -f docker/docker-compose.yml build

mode="$1"
clear="$2"

if [ "$mode" = "DB" ]; then
docker-compose -f docker/docker-compose.yml run --rm python python main.py --db handbook --user handbook_user --password 111111 --host postgres_db --port 5432
fi

if [ "$mode" = "XML" ]; then
docker-compose -f docker/docker-compose.yml run --rm python python main.py --path /handbook.xml
fi

if [ "$mode" = "" ] || [ "$mode" = "InMemory" ]; then
docker-compose -f docker/docker-compose.yml run --rm python python main.py
fi

if [ "$clear" = "clear" ]; then
docker-compose -f docker/docker-compose.yml down -v
else
docker-compose -f docker/docker-compose.yml stop
fi
