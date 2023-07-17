# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /DefiOSPython

COPY / /DefiOSPython
RUN python3 setup.py install

EXPOSE 5000

CMD cd DefiOSPython && python3 wsgi.py