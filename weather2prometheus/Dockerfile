FROM python:3-slim

RUN pip install requests prometheus_client

COPY run.py /app/
WORKDIR /app

CMD ["python", "-u", "run.py"]
