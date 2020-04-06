FROM ubuntu:18.04
LABEL maintainer="nobody@example.com"
ENV REFRESHED_AT 2020-04-06
RUN apt-get -yqq update && apt-get -yqq install nginx
RUN mkdir -p /var/www/html/website
ADD global.conf /etc/nginx/conf.d/
ADD nginx.conf /etc/nginx/
EXPOSE 80
