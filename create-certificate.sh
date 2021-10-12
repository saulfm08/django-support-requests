#!/bin/bash

openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out django_proj.crt \
            -keyout django_proj.key

gunicorn django_project.wsgi:application \
--certfile=django_proj.crt  \
--keyfile=django_proj.key \
--capture-output \
--bind 0.0.0.0:443