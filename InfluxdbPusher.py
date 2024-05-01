import influxdb_client, os, time, json, requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
token = 'iUjnOtambYUcVsZv1OEgJabl_hTjzaJNsoZYmi4y4CP73FZ2uI4KzDRDHzj7tXNDe4zhJPyDbdO7NteN7WhjVQ=='
org = "ORG_NAME"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# export INFLUX_TOKEN=6HGZtqXYPrEB4SOUrpdjZS8W2ATCVdVp3xnVd6bZOCV2YUFKVICY7AoJ7NBJuQrglY9i31u-nJfyX2HvQo4WgA==
# telegraf --config http://localhost:8086/api/v2/telegrafs/0cf04459a7212000

bucket="BUCKET2"
coincapapi= '2b9281b0-5c94-4017-944b-09681f69ecd9'
write_api = client.write_api(write_options=SYNCHRONOUS)

def get_bitcoin():
    url = "https://api.coincap.io/v2/assets/bitcoin"
    payload={}
    headers = {
    "Authorization": "Bearer "+coincapapi
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    # data = json.loads(response)
    price = data['data']['priceUsd']
    return price

while True:
  point = (
    Point("bitcoinprice")
    .tag("tagname1", "bitcoin")
    .field("price", int(float(get_bitcoin())))
    )
  write_api.write(bucket=bucket, org="ORG_NAME", record=point)
  time.sleep(1)
