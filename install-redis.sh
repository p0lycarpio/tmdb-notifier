#!/bin/sh

apt-get -y update
apt-get -y install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list

apt-get -y update
apt-get -y install redis

service redis-server stop
echo "unixsocket /run/redis.sock
unixsocketperm 775" >> /etc/redis/redis.conf
service redis-server start