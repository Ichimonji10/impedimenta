FROM python:3.8
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-12-03

ADD . /composeapp
WORKDIR /composeapp
RUN pip install flask redis
ENTRYPOINT [ "python", "app.py" ]
