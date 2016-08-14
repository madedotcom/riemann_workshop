#!/bin/sh
docker exec -it riemann s6-svc -t /var/run/s6/services/riemann
