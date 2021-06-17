#!/bin/sh

sysctl vm.overcommit_memory=1

echo never > /sys/kernel/mm/transparent_hugepage/enabled

redis-server /usr/local/etc/redis/redis.conf
