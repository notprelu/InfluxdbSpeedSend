There is a docker repo 

`docker run -d \
  --name speedtest-influx \
  --network host \
  --restart always \
  -e INFLUXDB_TOKEN=your_token \
  -e INFLUXDB_ORG=your_org \
  -e INFLUXDB_BUCKET=your_bucket \
  -e INFLUXDB_URL=http://localhost:8086 \
  matthewrb1/speedtestsender:latest
`
