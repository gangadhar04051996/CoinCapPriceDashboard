import json
import time
import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

time.sleep(10)
token = 'iUjnOtambYUcVsZv1OEgJabl_hTjzaJNsoZYmi4y4CP73FZ2uI4KzDRDHzj7tXNDe4zhJPyDbdO7NteN7WhjVQ=='
org = "ORG_NAME"
url = "http://influxdb:8086"
bucket = "bitcoinprice"
coincapapi = '2b9281b0-5c94-4017-944b-09681f69ecd9'
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=ASYNCHRONOUS)

def check_influxdb_ready():
    url = 'http://influxdb:8086/health'
    for _ in range(30):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("InfluxDB is ready.")
                return True
        except requests.exceptions.ConnectionError:
            print("Not Yet Ready")
            pass
        time.sleep(1)
    print("InfluxDB is not ready after 30 attempts.")
    return False

# Wait for InfluxDB to be ready
if not check_influxdb_ready():
    exit(1)

if client:
    print(True)

def get_coin_data():
    url = "https://api.coincap.io/v2/assets"
    payload = {}
    headers = {
        "Authorization": "Bearer " + coincapapi
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data["data"]

while True:
    coin_data = get_coin_data()

    # Process the data and write to InfluxDB
    for coin in coin_data:
        point = Point("crypto_prices") \
            .tag("currency", coin["symbol"]) \
            .field("rank", int(coin["rank"])) \
            .field("name", coin["name"]) \
            .field("supply", float(coin["supply"])) \
            .field("marketCapUsd", float(coin["marketCapUsd"])) \
            .field("volumeUsd24Hr", float(coin["volumeUsd24Hr"])) \
            .field("priceUsd", float(coin["priceUsd"])) \
            .field("changePercent24Hr", float(coin["changePercent24Hr"]))
        write_api.write(bucket=bucket, org=org, record=point)

    time.sleep(60)  # Wait for 1 minute before fetching data again

# Close the client
client.close()