FROM tensorflow/tensorflow:latest-gpu-py3

COPY docker/init.sh /etc/requirements.txt

SHELL ["/bin/bash", "-c"]
RUN apt install redis

RUN apt install cron
RUN python -m pip install --upgarde pip
RUN pip install -r /etc/requirements.txt

WORKDIR /django-app
