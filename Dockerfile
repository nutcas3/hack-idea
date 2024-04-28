FROM python:3.11.9-slim

ENV PYTHONUNBUFFERED=1

RUN apt -y update && apt -y install apt-utils && apt -y upgrade

RUN apt -y install python3 python3-pip

WORKDIR /onlineidea

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .