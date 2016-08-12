FROM debian:jessie

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    vim \
    iptables-dev \
    libcurl4-gnutls-dev \
    libdbi0-dev \
    libesmtp-dev \
    libgcrypt11-dev \
    libglib2.0-dev \
    libltdl-dev \
    liblvm2-dev \
    libmemcached-dev \
    libmnl-dev \
    libmodbus-dev \
    libmysqlclient-dev \
    libopenipmi-dev \
    liboping-dev \
    libow-dev \
    libpcap-dev \
    libperl-dev \
    libpq-dev \
    libprotobuf-c-dev \
    librabbitmq-dev \
    librrd-dev \
    libsensors4-dev \
    libsnmp-dev \
    libtokyocabinet-dev \
    libtokyotyrant-dev \
    libtool \
    libupsclient-dev \
    libvirt-dev \
    libxml2-dev \
    libyajl-dev \
    linux-libc-dev \
    pkg-config \
    protobuf-c-compiler \
    python-dev && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/info/* && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*

ENV COLLECTD_VERSION collectd-5.5.0

WORKDIR /tmp/

RUN curl -L https://collectd.org/files/${COLLECTD_VERSION}.tar.bz2 | tar -jx

WORKDIR $COLLECTD_VERSION
RUN ls


RUN ./configure && \
    make all && \
    make install && \
    make clean

RUN apt-get install python-psutil
ADD root /

CMD ["/opt/collectd/sbin/collectd", "-f"]
