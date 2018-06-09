FROM ubuntu:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

COPY . .

RUN sh scripts/build.sh

CMD [ "gunicorn", "server:app"]
