#!/bin/bash

/etc/init.d/redis-server start
gunicorn -c ./gunicorn/gunicorn.conf.py ai_django_redis.wsgi
