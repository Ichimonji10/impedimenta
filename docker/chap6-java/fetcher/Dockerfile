FROM ubuntu:18.04
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-12-06

RUN apt-get -yqq update
RUN apt-get -yqq install wget

WORKDIR /var/lib/tomcat8/webapps/

ENTRYPOINT [ "wget" ]
CMD [ "-?" ]
