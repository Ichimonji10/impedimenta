FROM ubuntu:18.04
LABEL maitainer="nobody@example.com"
ENV REFRESHED_AT 2020-04-08
RUN apt-get -yqq update && apt-get -yqq install redis-server redis-tools
EXPOSE 6379
ENTRYPOINT ["/usr/bin/redis-server"]
CMD []
