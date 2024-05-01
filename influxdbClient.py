import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = 'dO_cv6g_QPQBETbOsI2lwgjGHxYutr6JmojawX__wah7dh-Al1vDpEehD4fhsmT716IwNqjayBZbxzoxzjH9XQ=='
org = "ORG_NAME"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

query = """from(bucket: "BUCKET_NAME")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="ORG_NAME")

##for table in tables:
##  for record in table.records:
##    print(record)


query_api = client.query_api()

query = """from(bucket: "BUCKET_NAME")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="ORG_NAME")

for table in tables:
    for record in table.records:
        print(record)
