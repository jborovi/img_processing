#!/bin/bash
docker-compose -f docker-compose.prod.yml  -f docker-compose.yml up --build
