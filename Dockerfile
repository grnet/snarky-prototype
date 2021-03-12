FROM debian:buster

WORKDIR /snarky-ceremonies-dev

RUN apt-get update && apt-get install -y \
	vim \
	git \
	build-essential \
	libssl-dev \
	python3-dev \
	python3-pip

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt

COPY . .
