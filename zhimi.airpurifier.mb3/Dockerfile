FROM python:3-slim

RUN apt-get update && apt-get -y install build-essential libffi-dev libssl-dev
RUN pip install -U pip setuptools

RUN pip install prometheus_client python-miio

COPY *.py /app/

WORKDIR /app

CMD ["python", "-u", "run.py"]
