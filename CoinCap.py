
import requests
import json
import time
def get_bitcoin():
    url = "https://api.coincap.io/v2/assets/bitcoin"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.text
    data = json.loads(response)
    price = data['data']['priceUsd']
    print(f"The price is: {price}")

while True:
    get_bitcoin()
    time.sleep(1)
