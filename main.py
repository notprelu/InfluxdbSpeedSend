import subprocess
import json
import os
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

file_path = "speedtest_results.json"
url = "http://localhost:8086"
token = "uvzFFHlUOK9DPxlVJWWM6K9b5gUXas8LMnxLJaA531Gg5X1xCxHmHq7AMea0U9qP5_7pW0M3-BDIitp1SmeNSA=="
org = "test"
bucket = "test"

def run_speedtest():
    try:
        result = subprocess.run(["speedtest-cli", "--json"], capture_output=True, text=True)

        if not result.stdout.strip():
            raise ValueError("Speedtest returned empty JSON output.")

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format received from speedtest-cli.")

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print("Speedtest results saved to", file_path)

        with open(file_path, "r") as file:
            data = json.load(file)

        up = int(round(data.get("upload", 0) / 1_000_000, 0))
        down = int(round(data.get("download", 0) / 1_000_000, 0))

        print(f"Upload Speed: {up} Mbps")
        print(f"Download Speed: {down} Mbps")

        client = InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        point1 = Point("SpeedTest").tag("Type", "Upload").field("Upload", up)
        point2 = Point("SpeedTest").tag("Type", "Download").field("Download", down)

        write_api.write(bucket=bucket, org=org, record=[point1, point2])

        print("Data successfully written to InfluxDB!")

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File deleted successfully.")
        else:
            print("File not found.")

while True:
    run_speedtest()
    print("Waiting for 30 minutes before next test...")
    time.sleep(1800)
