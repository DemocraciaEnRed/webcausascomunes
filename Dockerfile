FROM alpine:3.9

RUN apk add --no-cache uwsgi-python3

RUN pip3 install --no-cache-dir flask flask-scss requests markdown2 python-dotenv
RUN pip3 install --no-cache-dir google-api-python-client google-auth-httplib2 google-auth-oauthlib


COPY . /app

WORKDIR /app

ENTRYPOINT ["uwsgi","--plugins", "python3", "--http-socket", "0.0.0.0:5000", "--wsgi-file", "run.py", "--callable", "app"]
