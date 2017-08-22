FROM python:3.5-alpine

RUN pip install prometheus_client requests

ENV BIND_PORT 9177

ADD src /app
WORKDIR /app

CMD ["python", "varnish_exporter.py"]
