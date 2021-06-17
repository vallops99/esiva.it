FROM redis:4.0.2

ENV AUTHOR valerio.farrotti@hotmail.it
ENV UPDATED 20210608

WORKDIR /

COPY redis.conf /usr/local/etc/redis/redis.conf
COPY docker-healthcheck.sh /usr/local/bin/

COPY run_redis.sh /run_redis.sh

HEALTHCHECK CMD ["/usr/local/bin/docker-healtcheck.sh"]
