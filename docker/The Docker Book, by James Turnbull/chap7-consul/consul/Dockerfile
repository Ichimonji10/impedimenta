FROM ubuntu:18.04
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-12-29

RUN apt-get -yqq update
RUN apt-get -yqq install curl unzip

ADD https://releases.hashicorp.com/consul/0.6.4/consul_0.6.4_linux_amd64.zip /tmp/consul.zip
RUN unzip /tmp/consul.zip -d /usr/sbin; chmod +x /usr/sbin/consul/; rm /tmp/consul.zip
ADD consul.json /config/

# Port and volume definitions have been moved to docker-compose.yml.
# EXPOSE 53/udp 8300 8301 8301/udp 8302 8302/udp 8400 8500

ENTRYPOINT ["/usr/sbin/consul", "agent", "-config-dir=/config"]
CMD []
