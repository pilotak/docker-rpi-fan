FROM python:3-alpine

WORKDIR /app

COPY . /app

RUN apk update \
&& apk add build-base raspberrypi \
&& pip3 install --trusted-host pypi.python.org -r requirements.txt \
&& apk del --purge build-base \
&& rm -rf /var/cache/apk/*

CMD ["python3", "-u", "fan.py"]