FROM jeanblanchard/java:jre-8u92
ENV RIEMANN_VERSION 0.2.11
RUN apk --update add curl \
    && curl -skL https://aphyr.com/riemann/riemann-${RIEMANN_VERSION}.tar.bz2 | bunzip2 | tar -x && \
    mv /riemann-${RIEMANN_VERSION} /opt/riemann
WORKDIR /opt/riemann
RUN sed -ie 's/env bash/env sh/' bin/riemann
RUN mkdir -p /opt/riemann/etc
ADD src/ /opt/riemann/etc

EXPOSE 5555 5555/udp 5556

WORKDIR /opt/riemann/etc/

ENTRYPOINT ["/opt/riemann/bin/riemann"]
CMD ["start"]
