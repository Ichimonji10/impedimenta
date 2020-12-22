FROM jaudet/redis-base
LABEL maintainer="jerebear@protonmail.com"
ENV REFRESHED_AT 2020-12-22

ENTRYPOINT [ \
    "redis-server", \
    "--protected-mode no", \
    "--logfile /var/log/redis/redis-replica.log", \
    "--slaveof redis-primary 6379"]
