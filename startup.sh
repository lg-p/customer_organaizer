#!/bin/sh

mode="$1"
clear="$2"

if [ "$mode" = "DB" ]; then
  printf "\nDB mode started: data is saved in the database."
  docker-compose -f docker/docker-compose.yml build
  docker-compose -f docker/docker-compose.yml run --rm python python main.py --db handbook --user handbook_user --password 111111 --host postgres_db --port 5432
fi

if [ "$mode" = "XML" ]; then
  printf "\nXML mode started: data is saved in an XML file."
  docker build -f docker/Dockerfile -t handbook_image .
  docker run -it --rm --name handbook_container handbook_image python main.py --path /handbook.xml
fi

if [ "$mode" = "" ] || [ "$mode" = "InMemory" ]; then
  printf "\nInMemory mode started: data is saved in internal memory."
  docker build -f docker/Dockerfile -t handbook_image .
  docker run -it --rm --name handbook_container handbook_image python main.py
fi

if [ "$mode" = "DB" ]; then
  if [ "$clear" = "clear" ]; then
    docker-compose -f docker/docker-compose.yml down -v
  else
    docker-compose -f docker/docker-compose.yml stop
  fi
fi
