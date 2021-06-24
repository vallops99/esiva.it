FROM python:3-alpine

ENV AUTHOR valerio.farrotti@gmail.com
ENV UPDATED 20210607

WORKDIR /usr/src/app/

RUN apk add --update yarn postgresql-libs gcc musl-dev postgresql-dev \
    libffi-dev zlib-dev jpeg-dev

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

RUN apk del -r postgresql

COPY . .

RUN mkdir -p /usr/src/app/media

# ENTRYPOINT ["tail", "-f", "/dev/null"]
