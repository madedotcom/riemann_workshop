#!/bin/sh
docker exec -it collectd s6-svc -h /var/run/s6/services/collectd
