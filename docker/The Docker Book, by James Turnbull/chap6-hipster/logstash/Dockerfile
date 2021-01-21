FROM ubuntu:18.04
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-12-22

RUN apt-get -yqq update
RUN apt-get -yqq install wget gnupg2 openjdk-8-jdk
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch \
    | apt-key add -
RUN echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" \
    | tee -a /etc/apt/sources.list.d/elastic-5.x.list
RUN apt-get -yqq update
RUN apt-get -yqq install logstash

WORKDIR /usr/share/logstash
ADD logstash.conf /usr/share/logstash/
ENTRYPOINT ["bin/logstash"]
CMD ["-f", "logstash.conf", "--config.reload.automatic"]
