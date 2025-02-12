# syntax=docker/dockerfile:1

FROM debian
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y curl && apt-get install -y python3 && apt-get install -y python3-pip
RUN pip install --no-input speedtest-cli --break-system-packages && pip install --no-input influxdb-client --break-system-packages
CMD ["python3", "main.py"]
