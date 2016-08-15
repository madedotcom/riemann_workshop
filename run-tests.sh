#!/bin/sh
docker exec -it riemann /opt/riemann/bin/riemann test /opt/riemann/etc/riemann-test.clj
