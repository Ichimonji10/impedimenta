FROM jenkins/jenkins:lts
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-10-05

USER root
RUN apt-get -qqy update; apt-get install -qqy sudo
RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers
RUN wget "https://get.docker.com/builds/Linux/x86_64/docker-latest.tgz"
RUN tar -vxzf docker-latest.tgz
RUN mv docker/* /usr/bin/

USER jenkins
# Script comes with parent image.
RUN /usr/local/bin/install-plugins.sh \
    chucknorris \
    git \
    git-client \
    greenballs \
    junit \
    ssh-slaves \
    ws-cleanup
