# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /DefiOSPython


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY /DefiOSPython /DefiOSPython


EXPOSE 5000

CMD [ "python3","mainapi.py"]