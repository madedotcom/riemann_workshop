#!/bin/sh
docker exec -it riemann /opt/riemann/bin/riemann test /etc/riemann/riemann-test.clj
