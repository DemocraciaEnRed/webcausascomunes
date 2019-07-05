#https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

RUN pip3 install flask-scss requests

COPY ./nginx-custom.conf /etc/nginx/conf.d
COPY ./uwsgi.ini /app
COPY ./app /app/app

