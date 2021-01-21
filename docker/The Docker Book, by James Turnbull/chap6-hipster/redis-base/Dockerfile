FROM ubuntu:18.04
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-12-22

RUN apt-get -yqq update
RUN apt-get -yqq install software-properties-common
RUN apt-add-repository ppa:chris-lea/redis-server
RUN apt-get -yqq update
RUN apt-get -yqq install redis-server redis-tools
