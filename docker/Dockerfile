FROM tensorflow/tensorflow:latest-gpu-py3

COPY requirements.txt /etc/requirements.txt

SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -y \
    redis \
    cron
RUN pip --no-cache-dir install --upgrade pip
RUN pip --no-cache-dir install -r /etc/requirements.txt
RUN sed -r 's/bind 127.0.0.1 ::1/bind 0.0.0.0/g' /etc/redis/redis.conf >> /etc/redis/redis1.conf
RUN rm -rf /etc/redis/redis.conf
RUN mv /etc/redis/redis1.conf /etc/redis/redis.conf
#RUN echo "never" > /sys/kernel/mm/transparent_hugepage/enabled

WORKDIR /django-app
