import influxdb_client, os, time, json, requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import logging

logging.log(level=2, msg="Contaier is set to Sleep 10 sec")
time.sleep(10)
token = 'iUjnOtambYUcVsZv1OEgJabl_hTjzaJNsoZYmi4y4CP73FZ2uI4KzDRDHzj7tXNDe4zhJPyDbdO7NteN7WhjVQ=='
org = "ORG_NAME"
url = "http://influxdb:8086"
bucket="bitcoinprice"
coincapapi= '2b9281b0-5c94-4017-944b-09681f69ecd9'
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

def check_influxdb_ready():
    url = 'http://influxdb:8086/health'
    for _ in range(30):  # Try 30 times
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("InfluxDB is ready.")
                return True
        except requests.exceptions.ConnectionError:
            print("Not Yet Ready")
            pass
        time.sleep(1)  # Wait for 1 second before retrying
    print("InfluxDB is not ready after 30 attempts.")
    return False

# Wait for InfluxDB to be ready
if not check_influxdb_ready():
    exit(1)

if client:
    print ( True)
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
