FROM ubuntu:18.04
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-12-22

RUN apt-get -yqq update
RUN apt-get -yqq install nodejs npm
RUN mkdir -p /var/log/nodeapp

ADD nodeapp /opt/nodeapp/

WORKDIR /opt/nodeapp
RUN npm install

ENTRYPOINT ["nodejs", "server.js"]
