#!/bin/sh
(cd python && docker build -t riemann_python .)
docker run -it --rm --link riemann riemann_python ash
